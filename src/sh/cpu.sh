#!/bin/bash
source $(dirname $0)/common.sh
sysbench cpu --threads=$cpu_num --cpu-max-prime=20000 run
