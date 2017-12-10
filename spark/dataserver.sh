#!/bin/sh

gzcat ~/projects/notebooks/data/bis/all.text.gz | nc -lk 9999
