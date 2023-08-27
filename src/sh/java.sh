#!/bin/bash

JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 /home/xuebling/.local/bin/esrally race --track=geonames --challenge=append-fast-with-conflicts --target-hosts=127.0.0.1:9200 --offline --kill-running-processes