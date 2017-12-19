#!/bin/bash -e

git clone https://github.com/Supervisor/supervisor.git /tmp/supervisor
cd /tmp/supervisor
python setup.py install
rm -rf /tmp/supervisor
