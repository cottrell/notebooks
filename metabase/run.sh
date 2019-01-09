#!/bin/bash
# docker version seems to work as of 2019-01 after the --network="host" was added.
#
# kubectl and helm both had issues.
#
#
# https://github.com/metabase/metabase/issues/8190
# https://discourse.metabase.com/
# https://metabase.com/docs/latest/troubleshooting-guide/datawarehouse.html

# https://github.com/metabase/metabase/blob/master/docs/operations-guide/running-metabase-on-docker.md

# need to map port on osx (I didn't do anything and it seems to have worked, maybe already have this setup)
# https://stackoverflow.com/questions/36286305/how-do-i-forward-a-docker-machine-port-to-my-host-port-on-osx
# localhost:3000
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
case $1 in
    docker)
        # docker run -d -p 3000:3000 --name metabase metabase/metabase
        # untested:
        metadata=$DIR/metadata
        mkdir -p $metadata
        docker run -d -p 3000:3000 --network="host" -v $metadata:/tmp -e "MB_DB_FILE=/tmp/metabase.db" --name metabase metabase/metabase
        ;;
    start)
        docker start metabase
        ;;
    stop)
        docker stop metabase
        ;;
    # kubectl)
    #     # https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/
    #     # TODO: WARNING: all metadata is lost need to mount or something !!! read about kubernetes PersistentVolumeClaims etc ... need to do docker line above
    #     # https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/
    #     kubectl run metabase-example --image=metabase/metabase --port=3000
    #     kubectl describe service metabase-example
    #     kubectl expose deployment metabase-example --type=LoadBalancer --name=my-service
    #     # kubectl expose deployment metabase-example --type=NodePort
    #     kubectl get services my-service
    #     kubectl describe services my-service
    #     kubectl get services my-service
    #     kubectl get pods --output=wide
    #     # INFO: connecting to postgres db from metabase was tricky only due to rabbit hole insinuating things about OSX. See
    #     # https://github.com/kubernetes/kubernetes/issues/67343#issuecomment-412582110
    #     # YOU SHOULD SIMPLY CONNECT TO LAN ADDRESS AS USUAL ... see notes in postgres make sure postgres is accepting connections etc.
    #     # 192.168.1.3 5432 for example. REMEMBER postgres password is probably set.
    #     # if you do the TODO above about persistent volumes this data will be persisted.
    #     ;;
    # ssh)
    #     kubectl exec -it metabase-example-67f87cf78-gzl29 -- /bin/bash
    #     ;;
    *)
        echo "prog docker|kubectl"
        ;;
esac
