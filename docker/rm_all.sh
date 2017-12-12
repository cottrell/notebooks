#!/bin/sh
docker-machine rm $(docker-machine ls -q) # Delete all VMs and their disk images
