#!/bin/sh
# https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside
docker run --name some-postgres -e POSTGRES_PASSWORD=secret -d -p 5432:5432 postgres

# docker exec -it some-postgres bash
# root@05b3a3471f6f:/# psql -U postgres
# postgres-# CREATE DATABASE mytest;
# postgres-# \q

# psql -h public-ip-server -p 5432 -U postgres

