#!/bin/bash -e
name=testproj
mkdir -p $name
cd $name
npm init --yes
npm install --save orbit-db ipfs
git init
echo node_modules > .gitignore
git add .gitignore
git commit -m 'initial' -a
