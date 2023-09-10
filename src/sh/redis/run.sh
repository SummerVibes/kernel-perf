#!/bin/bash
redis-benchmark -n 10000000 -r 10000 -q -d 512 -t set,get -c $(nproc)
