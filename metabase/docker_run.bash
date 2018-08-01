#!/bin/sh

# https://github.com/metabase/metabase/blob/master/docs/operations-guide/running-metabase-on-docker.md

# need to map port on osx (I didn't do anything and it seems to have worked, maybe already have this setup)
# https://stackoverflow.com/questions/36286305/how-do-i-forward-a-docker-machine-port-to-my-host-port-on-osx
docker run -d -p 3000:3000 --name metabase metabase/metabase
# localhost:3000
