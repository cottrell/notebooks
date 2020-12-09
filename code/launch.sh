#!/bin/bash
echo sudo systemctl start code-server@$USER
echo systemctl status code-server@$USER
sudo systemctl start code-server@$USER
systemctl status code-server@$USER
