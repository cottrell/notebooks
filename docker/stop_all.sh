#!/bin/sh

docker-machine stop $(docker-machine ls -q) # Stop all running VMs
