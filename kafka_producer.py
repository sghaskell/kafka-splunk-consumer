#!/usr/bin/env python
from pykafka import KafkaClient
import httplib
from random import randint
from datetime import datetime
import re

def readFile(log_file):
    fh = open(log_file, 'r')
    lines = fh.readlines()
    fh.close()
    return(lines)

def main():
    access_log_file = './access.log'
    dt_fmt = '%d/%b/%Y:%H:%M:%S'

    client = KafkaClient(hosts="172.17.0.2:9092,172.17.0.3:9093,172.17.0.4:9094")
    topic = client.topics['nginx']
    producer = topic.get_producer(use_rdkafka=True)

    access_logs = readFile(access_log_file)
    log_len = len(access_logs)
    while(True):
        try:
            rando = randint(0, log_len-1)
            rand_log = access_logs[rando]

            dtnow = datetime.now()
            new_time = dtnow.strftime(dt_fmt)
           
            rand_log = re.sub(r'\[([\d\w:\/]+)', '[%s' % new_time, rand_log)

            producer.produce(rand_log)
        except Exception as e:
            print "failed"
            continue

if __name__ == '__main__':

    main()
