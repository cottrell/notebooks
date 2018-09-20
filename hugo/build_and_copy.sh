#!/bin/sh -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/h
hugo
mkdir -p ../../docs/hugo
cp -vR public/* ../../docs/hugo
echo 'REMIND: git stuff'
