#!/bin/bash
time $(dirname $0)/pgfault -m 4 -t $(nproc) -i 40 -r
