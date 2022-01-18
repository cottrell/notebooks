#!/bin/sh
apt list --manual-installed | sed 's/\// /' | awk '{print $1 "=" $3}'
