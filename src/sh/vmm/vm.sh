#!/bin/bash

timeout -s SIGKILL 60s qemu-system-x86_64 -m 8G -nographic -monitor none -hda $(dirname $0)/openEuler-22.03-LTS-SP2-x86_64.qcow2 || true
