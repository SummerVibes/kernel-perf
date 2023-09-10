#!/bin/bash
time $(dirname $0)/pgfault -m 8 -t "$(nproc)" -i 40 -r