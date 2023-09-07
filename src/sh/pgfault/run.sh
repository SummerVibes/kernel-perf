#!/bin/bash
# sysbench memory --memory-block-size=8K run
# stress-ng -vm 4 --vm-bytes 4G --timeout 30s
$(dirname $0)/pgfault -m 4 -t "$(nproc)" -i 40
 