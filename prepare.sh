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

function install_slim() {
    wget https://downloads.dockerslim.com/releases/1.40.2/dist_linux.tar.gz
}

install_package
install_docker