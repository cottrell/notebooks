#!/bin/bash

# Find all .gitignore files and check for 'joblib' in them
find . -type f -name ".gitignore" -exec grep -l "Created by joblib automatically" {} \;
