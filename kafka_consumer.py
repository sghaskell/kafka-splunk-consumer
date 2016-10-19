#!/usr/bin/env python
from pykafka import KafkaClient
import logging
import multiprocessing
from splunkhec import hec
import argparse
import sys
import yaml
from pprint import pprint

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
                 batch_size=1024):

        self.batch_size = batch_size
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
        self.initLogger()

    def initLogger(self):
        log_format = '%(asctime)s name=%(name)s loglevel=%(levelname)s message=%(message)s'
        logging.basicConfig(format=log_format,
                            level=logging.DEBUG)

    def consume(self):
        topic = self.client.topics[self.topic]

        consumer = topic.get_balanced_consumer(zookeeper_connect=self.zookeeper_server, 
                                                 consumer_group=self.consumer_group,
                                                 use_rdkafka=self.use_rdkafka)

        # create splunk hec instance
        splunk_hec = hec(self.splunk_server,
                         self.splunk_hec_port,
                         self.splunk_hec_channel,
                         self.splunk_hec_token,
                         self.splunk_sourcetype,
                         self.splunk_source)
        while(True):
            m = consumer.consume()
            if(len(self.messages) < self.batch_size):
                self.messages.append(m.value)
            else:
                # write batch of batch_size messages to HEC
                status_code = splunk_hec.writeToHec(self.messages)

                if(status_code == 200):
                    # Clear out messages
                    self.messages = []

                    # commit offsets in Kafka
                    consumer.commit_offsets()
                else:
                    logging.error("Failed to send events to Splunk HTTP Event Collector. Verify server, port, token and channel are correct")

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
                             config['general']['batch_size'])

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
