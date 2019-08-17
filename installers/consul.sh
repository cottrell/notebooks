#!/bin/sh
cd /tmp
wget https://releases.hashicorp.com/consul/1.4.0/consul_1.4.0_linux_amd64.zip
unzip consul_1.4.0_linux_amd64.zip
sudo mv consul /usr/localb/bin
