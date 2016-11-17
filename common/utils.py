"""
Author: Scott Haskell
Company: Splunk Inc.

Module that contains helper utilities.
"""

__license__ = """
The MIT License

Copyright (c) 2016 Scott Haskell, Splunk Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import argparse
import yaml
import sys

def parseArgs():
    """ Parse command line arguments 
    Returns:
    flags -- parsed command line arguments
    """
    argparser = argparse.ArgumentParser() 
    argparser.add_argument('-c',
                           '--config',
                           default='kafka_consumer.yml',
                           help='Kafka consumer config file')
    flags = argparser.parse_args()
    return(flags)

def parseConfig(config):
    """ Parse YAML config 
    Arguments:
    config (string) -- path to YAML config

    Returns:
    parsed YAML config file
    """
    try:
        with open(config, 'r') as stream:
            try:
                return(yaml.load(stream))
            except yaml.YAMLError as exc:
		sys.stderr.write("Failed to parse config file %s" % sys.argv[1])
    except IOError as e:
        sys.stderr.write("I/O error(%s): %s %s\n" % (e.errno, e.strerror, e.filename))
        sys.stderr.write("Usage: %s -c <config.yml>\n" % (sys.argv[0]))
        sys.exit(-1)
