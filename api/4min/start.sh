#!/bin/sh

file=$1
[[ "$file" ]] || file=swagger.yml
python backend.py -p 5000 -s $file

