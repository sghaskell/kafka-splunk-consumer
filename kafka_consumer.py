#!/usr/bin/env python
from pykafka import KafkaClient
import logging
import multiprocessing
from splunkhec import hec
import argparse
import sys
import yaml
from redo import retry

jobs = []

def parseArgs():
    argparser = argparse.ArgumentParser() 
    argparser.add_argument('-c',
                           '--config',
                           default='kafka_consumer.yml',
                           help='Kafka consumer config file')
    flags = argparser.parse_args()
    return(flags)

class kafkaConsumer:
    def __init__(self,
                 brokers=[],
                 zookeeper_server="",
                 topic="",
                 consumer_group="",
                 use_rdkafka=False,
                 splunk_server="",
                 splunk_hec_port="8088",
                 splunk_hec_channel="",
                 splunk_hec_token="",
                 splunk_sourcetype="",
                 splunk_source="",
                 batch_size=1024,
                 retry_attempts=5,
                 sleeptime=60,
                 max_sleeptime=300,
                 sleepscale=1.5,
                 jitter=1):
        self.messages = []
        self.brokers = brokers
        self.client = KafkaClient(hosts=','.join(self.brokers))
        self.zookeeper_server = zookeeper_server
        self.topic = topic
        self.consumer_group = consumer_group
        self.use_rdkafka = use_rdkafka
        self.splunk_server = splunk_server
        self.splunk_hec_port = splunk_hec_port
        self.splunk_hec_channel = splunk_hec_channel
        self.splunk_hec_token = splunk_hec_token
        self.splunk_sourcetype = splunk_sourcetype
        self.splunk_source = splunk_source
        self.batch_size = batch_size
        self.retry_attempts=retry_attempts
        self.sleeptime=sleeptime
        self.max_sleeptime=max_sleeptime
        self.sleepscale=sleepscale
        self.jitter=jitter
        self.consumer_started = False
        self.initLogger()

    def initLogger(self):
        log_format = '%(asctime)s name=%(name)s loglevel=%(levelname)s message=%(message)s'
        logging.basicConfig(format=log_format,
                            level=logging.DEBUG)

    def getConsumer(self, topic):
        consumer = topic.get_balanced_consumer(zookeeper_connect=self.zookeeper_server, 
                                               consumer_group=self.consumer_group,
                                               use_rdkafka=self.use_rdkafka)
        self.consumer_started = True
        return consumer

    def sendToSplunk(self,
                     splunk_hec):
        # Initialize and start consumer if down
        if(not self.consumer_started):
            self.consumer = self.getConsumer(self.client.topics[self.topic])

        # Attempt to send messages to Splunk
        status_code = splunk_hec.writeToHec(self.messages)

        # clear messages
        self.messages = []

        # Check for successful delivery
        if(status_code == 200):
            # commit offsets in Kafka
            self.consumer.commit_offsets()
            return
        else:
            # Stop consumer and mark it down
            self.consumer.stop()
            self.consumer_started = False

            # Raise exception for retry
            logging.error("Failed to send data to Splunk HTTP Event Collector - check host, port, token & channel")
            raise Exception('Failed to send data to Splunk HTTP Event Collector - Retrying')


    def consume(self):
        self.consumer = self.getConsumer(self.client.topics[self.topic])

        # create splunk hec instance
        splunk_hec = hec(self.splunk_server,
                         self.splunk_hec_port,
                         self.splunk_hec_channel,
                         self.splunk_hec_token,
                         self.splunk_sourcetype,
                         self.splunk_source)
        while(True):
            m = self.consumer.consume()

            if(len(self.messages) < self.batch_size):
                self.messages.append(m.value)
            else:
                retry(self.sendToSplunk,
                      attempts=self.retry_attempts,
                      sleeptime=self.sleeptime,
                      max_sleeptime=self.max_sleeptime,
                      sleepscale=self.sleepscale,
                      jitter=self.jitter,
                      retry_exceptions=(Exception,),
                      args=(splunk_hec,))

def worker(num, config):
    worker = "Worker-%s" % (num)
    print(worker)
    consumer = kafkaConsumer(config['kafka']['brokers'],
                             config['kafka']['zookeeper_server'],
                             config['kafka']['topic'],
                             config['kafka']['consumer_group'],
                             config['kafka']['use_rdkafka'],
                             config['hec']['host'],
                             config['hec']['port'],
                             config['hec']['channel'],
                             config['hec']['token'],
                             config['hec']['sourcetype'],
                             config['hec']['source'],
                             config['general']['batch_size'],
                             config['network']['retry_attempts'],
                             config['network']['sleeptime'],
                             config['network']['max_sleeptime'],
                             config['network']['sleepscale'],
                             config['network']['jitter'])

    consumer.consume()

def parseConfig(config):
    with open(config, 'r') as stream:
        try:
            return(yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)

def main():
    flags = parseArgs()
    config = parseConfig(flags.config)
    multiprocessing.log_to_stderr(logging.INFO)
    num_workers = config['general']['workers']
    
    for i in range(num_workers):
        worker_name = "worker-%s" % i
        p = multiprocessing.Process(name=worker_name, target=worker, args=(i,config))
        jobs.append(p)
        p.start()

    for j in jobs:
        j.join()

if __name__ == '__main__':
    main()
