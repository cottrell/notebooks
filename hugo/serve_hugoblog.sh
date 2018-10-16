#!/bin/sh -e
# run this FROM the hugo dir!
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/hugoblog
hugo server --buildDrafts -w --forceSyncStatic
