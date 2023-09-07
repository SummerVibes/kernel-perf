#!/bin/bash
source $(dirname $0)/common.sh

redis-benchmark -n 1000000 -q --csv
