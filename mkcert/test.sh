#!/bin/bash
type http-server || npm i -g http-server
http-server -S -C localhost+3.pem -K localhost+3-key.pem
