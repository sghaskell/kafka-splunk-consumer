## Kafka Consumer For Splunk
### Description
A Kafka consumer that implements a pykafka balanced consumer and Python multiprocessing to send messages to Splunk HTTP Event collector tier with scalability, parallelism and high availability in mind.

### Compatibility
* Splunk >= 6.4.0 (uses [HEC Raw endpoint](http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTinput#services.2Fcollector.2Fraw))
* Kafka >= 0.8.2
* Developed against Kafka 0.10.0.0
* Requires Zookeeper to balance multiple consumers

### Dependencies
* [Python >= 2.7](https://www.python.org/downloads/)
* [pykafka](https://github.com/Parsely/pykafka)
* [Python Requests](http://docs.python-requests.org/en/master/)
* [PyYaml](http://pyyaml.org/)
* [redo](https://pypi.python.org/pypi/redo)
* [splunkhec](https://github.com/sghaskell/kafka-splunk-consumer/blob/master/splunkhec.py)

#### Optional
* [python-snappy](https://pypi.python.org/pypi/python-snappy) - support for snappy compression
* [librdkafka](https://github.com/edenhill/librdkafka) - Speed up consumer using C wrapper around librdkafka. [See docs for details](http://pykafka.readthedocs.io/en/latest/roadmap.html?highlight=rdkafka#pure-python-vs-rdkafka).

### Limitations
* Currently reads earliest offset from queue (all messages) on first run. ([See enhancement](https://github.com/sghaskell/kafka-splunk-consumer/issues/2))
* Supports one Splunk HTTP Event Collecor host.
  * A scalable and highly available HEC tier should be behind a VIP/load balancer. Please reference the following articles:
    * [High volume HTTP Event Collector Using Load Balancer](http://dev.splunk.com/view/event-collector/SP-CAAAE9Q)
    * [Configure an NGINX load balancer for HEC](http://dev.splunk.com/view/event-collector/SP-CAAAE9Q)

### Configuration
See comments in the [sample YAML file](https://github.com/sghaskell/kafka-splunk-consumer/blob/master/kafka_consumer.yml) for all available configuration options.

### Usage
```bash
$ python kafka_consumer.py [-f <config.yml>]
```

### Deployment Guidance
This script can be run on as many servers as you like to scale out consuming from your Kafka topics. The script uses Python multiprocessing to take advantage of multiple cores. Configure as many instances of the script on as many servers as necessary to scale out consuming large volumes of messages. Do not exceed more workers than cores available for a given server. The number of workers across all your instances of the script should not exceed the number of partitions for a given topic. If you configure more workers than the number of partitions in the topic, you will have idle workers that will never get assigned to consume from a topic.

The splunk HTTP Event Collector should be deployed as a tier of collectors behind a VIP or load balancer. See the links in the [Limitations](https://github.com/sghaskell/kafka-splunk-consumer#limitations) section above for architrecture guidance.

For more information on the specifics of the pykafka balanced consumer and its benefits, see [this section of the docs](http://pykafka.readthedocs.io/en/latest/roadmap.html#simpleconsumer-vs-balancedconsumer).

If you have a busy topic and you're not getting the throughput you had hoped, consider disabling HTTPS for your HTTP Event Collector tier to see if that speeds up ingest rates. (see [`use_https`](https://github.com/sghaskell/kafka-splunk-consumer/blob/master/kafka_consumer.yml#L42))

### Bugs & Feature Requests
Please feel free to file bugs or feature requests if something isn't behaving or there's a shortcoming feature-wise.
