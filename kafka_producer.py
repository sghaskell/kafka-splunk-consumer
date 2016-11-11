#!/usr/bin/env python
# Author: Scott Haskell
# Company: Splunk Inc.
# Date: 2016-10-21
#
# The MIT License
#
# Copyright (c) 2016 Scott Haskell, Splunk Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
from pykafka import KafkaClient
import httplib
from random import randint
from datetime import datetime
import re

# Update with your topic
TOPIC = "nginx" 

# Update with your list of Kafka brokers <host>:<port>
KAFKA_HOSTS = "172.17.0.2:9092,172.17.0.3:9093,172.17.0.4:9094"

# Use rdkafka if pykafka is built against librdkafka
USE_RDKAFKA = True

def readFile(log_file):
    """ open file and return contents """

    fh = open(log_file, 'r')
    lines = fh.readlines()
    fh.close()
    return(lines)

def main():
    """ Simple Kafka producer to publish random NGINX events from access.log for testing """

    access_log_file = './access.log'
    dt_fmt = '%d/%b/%Y:%H:%M:%S'

    client = KafkaClient(hosts=KAFKA_HOSTS)

    topic = client.topics[TOPIC]
    producer = topic.get_producer(use_rdkafka=USE_RDKAFKA)

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
        except (KeyboardInterrupt, SystemExit):
            raise Exception("Exit via ctrl-c from user")

if __name__ == '__main__':
    main()
