#!/bin/bash

cat /proc/meminfo | grep "ZeroedFree"
cat /proc/meminfo | grep "ZeroedTHPFree"
dmesg | grep "kzerod"