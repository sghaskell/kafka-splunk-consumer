from setuptools import setup, find_packages

# Information Configuration Goes Here
author = "Scott Haskell"
author_email = "shaskell@splunk.com"
version = "0.3b"
classifiers = ["Development Status :: 4 - Beta",
               "Environment :: Console",
               "Intended Audience :: Developers",
               "Intended Audience :: End Users/Desktop",
               "License :: OSI Approved :: MIT License",
               "Natural Language :: English",
               "Operating System :: MacOS",
               "Operating System :: Microsoft",
               "Operating System :: Unix",
               "Programming Language :: Python :: 2.7",
               "Topic :: Utilities"]
description = "A Kafka consumer that implements a pykafka balanced consumer and Python multiprocessing to send messages to Splunk HTTP Event collector tier with scalability, parallelism and high availability in mind."
download_url = "https://github.com/sghaskell/kafka-splunk-consumer/archive/master.zip"
home_page_url = "https://github.com/sghaskell/kafka-splunk-consumer"
# Specifies installation library dependencies
install_requirements = ["pyyaml>=3.12",
                        "pykafka>=2.5.0",
                        "requests>=2.12.1",
                        "requests>=2.12.1",
                        "redo>=1.6"]
keywords = ["Kafka",
            "Splunk",
            "HTTP Event Collector"]
license = "MIT"
name = "kafka-splunk-consumer"
packages = ['splunkhec']
platforms = ["MacOS",
             "Microsoft",
             "Unix"]
data_files = [('config', ['config/kafka_consumer.yml']),
              ('config', ['config/access.log'])]
scripts = ["scripts/kafka_splunk_consumer"]

# Setup tools configuration goes here
setup(
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    description=description,
    download_url=download_url,
    install_requires=install_requirements,
    keywords=keywords,
    license=license,
    name=name,
    packages=find_packages(),
    data_files=data_files,
    platforms=platforms,
    url=home_page_url,
    scripts=scripts,
    version=version
)
