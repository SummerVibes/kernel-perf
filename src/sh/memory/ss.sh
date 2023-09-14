#!/bin/bash
time $(dirname $0)/pgfault -m 1 -t "$(nproc)" -i 1
 
