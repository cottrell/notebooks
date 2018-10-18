#!/bin/sh -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/hugoblog
hugo
mkdir -p ../../docs
cp -vR public/* ../../docs
echo 'REMINDER: git stuff'
