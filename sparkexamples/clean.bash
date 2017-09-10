#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
rm -rf $DIR/{__pycache__,cp,out,metastore_db,derby.log,data}
