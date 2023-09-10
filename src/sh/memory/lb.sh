#!/bin/bash
# sysbench memory --memory-block-size=8K run
# stress-ng -vm 4 --vm-bytes 4G --timeout 30s
time $(dirname $0)/pgfault -m 8 -t "$(nproc)" -i 40
 