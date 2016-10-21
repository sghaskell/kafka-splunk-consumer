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

        return res.status_code
