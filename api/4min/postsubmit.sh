#!/bin/sh
# pip install flask # already done
pip install -r python-flask-server/requirements.txt
pip install flask-cors
mv python-flask-server/swagger_server swagger_server
rm -rf python-flask-server
# then modify main.py
