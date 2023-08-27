#!/bin/bash
source $(dirname $0)/common.sh
sysbench memory --memory-block-size=8K run
