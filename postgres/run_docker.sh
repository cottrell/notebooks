#!/bin/sh
# https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside

DOCKER_VOLUME=$HOME/docker/volumes/postgres
mkdir -p $DOCKER_VOLUME
PORT=15432

case $1 in
    # init)
    #     pg_ctl -D $dbdir -l $logfile initdb
    #     ;;
    start)
        echo WARNING: use some external password store. this hard coded password is just for kicks!
        docker run --rm --name pg-docker -e POSTGRES_PASSWORD=secret -d -p $PORT:5432 -v $DOCKER_VOLUME:/var/lib/postgresql/data postgres
        ;;
    connect)
        psql -p $PORT -h localhost -U postgres -d postgres
        # psql postgres
        ;;
    stop)
        pg_ctl -D $dbdir stop
        ;;
    *)
        echo dunno
        exit 1
        ;;
esac


# docker exec -it some-postgres bash
# root@05b3a3471f6f:/# psql -U postgres
# postgres-# CREATE DATABASE mytest;
# postgres-# \q

# psql -h public-ip-server -p 5432 -U postgres

