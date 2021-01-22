#!/bin/sh -e
cd /app/books
python -m http.server --bind 0.0.0.0 $*
