#!/bin/bash -e
# https://johnpapa.net/node-and-npm-without-sudo/
# manual: Install Node.js from https://nodejs.org/en/download/
sudo npm install npm -g
mkdir -p ~/.npm-packages
npm config set prefix ~/.npm-packages
npm install @vue/cli @vue/cli-service -g
