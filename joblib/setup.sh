#!/bin/bash
for x in 1 2 3; do
    echo "[ -e joblib_cache$x ] && (chmod -R a+w joblib_cache$x && dl joblib_cache$x)"
    echo cp -v joblib_cache joblib_cache$x -R
    echo chmod -R a-w joblib_cache$x
done
