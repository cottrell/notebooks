#!/bin/sh -e
DIR="$( cd "$( dirname $(realpath "${BASH_SOURCE[0]}") )" && pwd )"
cd $DIR
if [ $(uname) = 'Darwwin' ]; then
    ip=$(ipconfig getifaddr en1)
else
    ip=$(hostname -I | cut -d' ' -f1)
fi
port=1313
hugo server --buildDrafts -w --disableFastRender --forceSyncStatic --bind=$ip --baseURL="http://$ip:$port" --port $port $@
cd -
