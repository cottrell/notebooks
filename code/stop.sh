#!/bin/bash
sudo systemctl stop code-server@$USER
systemctl status code-server@$USER
