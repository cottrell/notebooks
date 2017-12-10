#!/bin/sh
docker pull dgraph/dgraph

# Now, to run Dgraph in Docker, it’s:
mkdir -p ~/dgraph

trap "kill -- -$$" EXIT

# Run dgraphzero
docker run -it -p 8080:8080 -p 9080:9080 -v ~/dgraph:/dgraph --name dgraph dgraph/dgraph dgraph zero --port_offset=-2000

# In another terminal, now run dgraph

docker exec -it dgraph dgraph server --bindall=true --memory_mb 2048 --zero localhost:5080

# clean up
# docker ps -aq --no-trunc | xargs docker rm

