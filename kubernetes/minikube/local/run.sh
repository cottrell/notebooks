#!/bin/sh

# more concrete notes

case $1 in
    dashboard-create)
        kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
        ;;
    dashboard-forward)
        # forward a pod port to local host
        # TODO: the name will change, you need to get it somehow
        # kubectl get all --all-namespaces
        # kubectl get pods --namespace=kube-system
        kubectl port-forward kubernetes-dashboard-7d5dcdb6d9-grxsw 8443:8443 --namespace=kube-system
        ;;
    *)
        echo dunno
        ;;
esac

