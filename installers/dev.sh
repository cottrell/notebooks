#!/bin/bash -e
# ~/dev or ~/code
cd ~/dev
hub clone automl/auto-sklearn
cd ~/dev/tensorflow
[[ -e tensorflow ]] || hub clone tensorflow/tensorflow
[[ -e probability ]] || hub clone tensorflow/probability
[[ -e models ]] || hub clone tensorflow/models
git clone https://github.com/hootnot/saxo_openapi.git
