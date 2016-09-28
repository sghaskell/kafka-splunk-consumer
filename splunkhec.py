import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import logging

class hec:
    def __init__(self,
                 splunk_server="",
                 splunk_hec_port="8088",
                 splunk_hec_channel="",
                 splunk_hec_token="",
                 splunk_sourcetype="",
                 splunk_source=""):

        self.splunk_server = splunk_server
        self.splunk_hec_port = splunk_hec_port
        self.splunk_hec_channel = splunk_hec_channel
        self.splunk_hec_token = splunk_hec_token
        self.splunk_sourcetype = splunk_sourcetype
        self.splunk_source = splunk_source
        self.token_string = "Splunk %s" % self.splunk_hec_token
        self.post_string = 'https://%s:%s/services/collector/raw?\
channel=%s&sourcetype=%s&source=%s' % (self.splunk_server,
                                       self.splunk_hec_port,
                                       self.splunk_hec_channel,
                                       self.splunk_sourcetype,
                                       self.splunk_source)


    def writeToHec(self, messages):
        res = requests.post(self.post_string,
                            data = '\n'.join(messages),
                            verify = False,
                            headers = {'Authorization' : self.token_string})
        logging.debug("wrote %s messages to HEC at %s" % (len(messages),
                                                             self.post_string))
