#!/bin/bash
set -e
cpu_num=$(lscpu -p | grep -c '^[0-9]')