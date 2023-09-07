#!/bin/bash
source $(dirname $0)/common.sh

time redis-benchmark -n 1000000 -q
