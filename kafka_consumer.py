#!/usr/bin/env python
from pykafka import KafkaClient
import logging
import multiprocessing
from splunkhec import hec

jobs = []
brokers = ["172.17.0.2:9092","172.17.0.3:9093","172.17.0.4:9094"]
zookeeper_server = "localhost:2181"
topic = "nginx"
consumer_group = "shark"
use_rdkafka = True
splunk_server = "172.17.0.5"
splunk_hec_port = "8088"
splunk_hec_channel = "0cadab76-3a7b-4561-ba8a-aa3fed09cb59"
splunk_hec_token = "B373AE38-902D-4DFC-87BE-43E0E5D5AB09"
splunk_sourcetype = "access_combined"
splunk_source = "hec:nginx"

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
                            level=logging.INFO)

    def consume(self):
        topic = self.client.topics[self.topic]

        consumer = topic.get_balanced_consumer(zookeeper_connect=self.zookeeper_server, 
                                                 consumer_group=self.consumer_group,
                                                 use_rdkafka=self.use_rdkafka)

        # create splunk hec instance
        splunk_hec = hec(splunk_server,
                         splunk_hec_port,
                         splunk_hec_channel,
                         splunk_hec_token,
                         splunk_sourcetype,
                         splunk_source)
        while(True):
            m = consumer.consume()
            if(len(self.messages) < self.batch_size):
                self.messages.append(m.value)
            else:
                # write batch of batch_size messages to HEC
                splunk_hec.writeToHec(self.messages)

                # Clear out messages
                self.messages = []

                # commit offsets in Kafka
                consumer.commit_offsets()

def worker(num):
    worker = "Worker-%s" % (num)
    print(worker)
    consumer = kafkaConsumer(brokers,
                             zookeeper_server,
                             topic,
                             consumer_group,
                             use_rdkafka,
                             splunk_server,
                             splunk_hec_port,
                             splunk_hec_channel,
                             splunk_hec_token,
                             splunk_sourcetype,
                             splunk_source)

    consumer.consume()

def main():
    multiprocessing.log_to_stderr(logging.INFO)

    for i in range(3):
        worker_name = "worker-%s" % i
        p = multiprocessing.Process(name=worker_name, target=worker, args=(i,))
        jobs.append(p)
        p.start()

    for j in jobs:
        j.join()

if __name__ == '__main__':

    main()
