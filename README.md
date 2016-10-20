## Kafka Consumer For Splunk
### Compatibility
* Kafka >= 0.8.2
* Developed against Kafka 0.10.0.0

### Dependencies
* [Python >= 2.7](https://www.python.org/downloads/)
* [pykafka](https://github.com/Parsely/pykafka)
* [Python Requests](http://docs.python-requests.org/en/master/)
* [PyYaml](http://pyyaml.org/)
* [redo](https://pypi.python.org/pypi/redo)
* [splunkhec](https://github.com/sghaskell/kafka-splunk-consumer/blob/master/splunkhec.py)

### Limitations
* Does not currently support TLS connections to Kafka
* Supports one Splunk HTTP Event Collecor host.
  * A highly available HEC tier should be behind a VIP/load balancer. Please reference the following articles
    * [High volume HTTP Event Collector Using Load Balancer](http://dev.splunk.com/view/event-collector/SP-CAAAE9Q)
    * [Configure an NGINX load balancer for HEC](http://dev.splunk.com/view/event-collector/SP-CAAAE9Q)
