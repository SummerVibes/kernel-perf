#!/bin/bash

set -e

function install_package() {
    sudo apt install -y git sysstat fio lshw python3 mbw sysbench
    sudo pip3 install -r requirements.txt
}

function install_docker() {
    sudo curl -fsSL https://get.docker.com | sudo bash -s docker --mirror Aliyun
    sudo systemctl start docker
    sudo systemctl enable docker
}

sudo so
install_package
install_docker