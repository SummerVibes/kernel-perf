#!/bin/bash
time $(dirname $0)/pgfault -m 2 -t "$(nproc)" -i 40
 