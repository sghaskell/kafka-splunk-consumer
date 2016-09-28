#!/usr/bin/env python
from pykafka import KafkaClient
import requests
import logging
import multiprocessing

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
                 splunk_source=""):
        self.max_len = 1024
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

    def consume(self):
        topic = self.client.topics[self.topic]

        consumer = topic.get_balanced_consumer(zookeeper_connect=self.zookeeper_server, 
                                                 consumer_group=self.consumer_group,
                                                 use_rdkafka=self.use_rdkafka)
        while(True):
            m = consumer.consume()
            if(len(self.messages) < self.max_len):
                self.messages.append(m.value)
            else:
                token_string = "Splunk %s" % self.splunk_hec_token
                post_string = 'https://%s:%s/services/collector/raw?channel=%s&sourcetype=%s&source=%s' % (self.splunk_server, self.splunk_hec_port, self.splunk_hec_channel, self.splunk_sourcetype, self.splunk_source)
 

                res = requests.post(post_string,
                                    data = '\n'.join(self.messages),
                                    verify = False,
                                    headers = {'Authorization' : token_string}
                                   )
                self.messages = []
     
def main():
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

    kconsumer = kafkaConsumer(brokers,
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
    kconsumer.consume()

if __name__ == '__main__':

    main()
