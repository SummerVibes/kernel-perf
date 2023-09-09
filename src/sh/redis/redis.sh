#!/bin/bash

redis-benchmark -n 10000000 -q -d 512 -t set,get -c $(nproc)