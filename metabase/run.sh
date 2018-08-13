#!/bin/sh
# https://discourse.metabase.com/
# https://metabase.com/docs/latest/troubleshooting-guide/datawarehouse.html
# https://github.com/metabase/metabase/blob/master/docs/operations-guide/running-metabase-on-docker.md
# need to map port on osx (I didn't do anything and it seems to have worked, maybe already have this setup)
# https://stackoverflow.com/questions/36286305/how-do-i-forward-a-docker-machine-port-to-my-host-port-on-osx
# localhost:3000
case $1 in
    docker)
        docker run -d -p 3000:3000 --name metabase metabase/metabase
        ;;
    kubectl)
        # https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/
        kubectl run metabase-example --image=metabase/metabase --port=3000
        kubectl describe service metabase-example
        kubectl expose deployment metabase-example --type=LoadBalancer --name=my-service
        # kubectl expose deployment metabase-example --type=NodePort
        kubectl get services my-service
        kubectl describe services my-service
        kubectl get services my-service
        kubectl get pods --output=wide
        # localhost:3000
        echo to ssh into machine do something like kubectl exec -it metabase-example-67f87cf78-gzl29 -- /bin/bash
        ;;
    ssh)
        kubectl exec -it metabase-example-67f87cf78-gzl29 -- /bin/bash
        ;;
    *)
        echo "prog docker|kubectl"
        ;;
esac
