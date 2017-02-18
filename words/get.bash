#!/bin/bash
set -e
# wget http://www.gutenberg.org/dirs/etext02/mthes10.zip
# mkdir data
# mv mthes10.zip data
cd data
unzip mthes10.zip
cat mthesaur.txt | tr ',' '\n' | python -c 'import sys; seen = set(); [print(x.strip()) for x in sys.stdin if x not in seen and not seen.add(x)]' | sort -u > allwords.txt
cd -
./p.py
