#!/bin/bash

timeout -s SIGKILL 60s qemu-system-x86_64 -m 8G -nographic -monitor none -hda $(dirname $0)/alpine-virt-3.18.3-x86_64.iso || true