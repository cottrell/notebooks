#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# had to force the link to update it
case $1 in
    install)
        brew install kubectl
        brew link --overwrite kubernetes-cli
        if [ "$(uname)" = "Darwin" ]; then
            brew tap pachyderm/tap && brew install pachyderm/tap/pachctl@1.7
        else
            curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v1.7.1/pachctl_1.7.1_amd64.deb && sudo dpkg -i /tmp/pachctl.deb
        fi
        ;;
    minikube_start)
        minikube stop
        minikube delete
        minikube start
        ;;
    pachctl_start)
        pachctl deploy local
        kubectl get pods
        pachctl port-forward &
        ;;
    update_pipelines)
        # how to do all at once?
        for x in $(ls $DIR/pipelines/*); do
            pachctl update-pipeline -f $x
        done
        ;;
    *)
        echo "do.sh install|pachctl_start|minikube_start"
        echo "do you want to bounce restart (y/n)? "
        read answer
        if [[ "$answer" = 'y' ]]; then
            ${BASH_SOURCE[0]} minikube_start
            ${BASH_SOURCE[0]} pachtl_start
        fi
        ;;
esac

# get errors unable to decode "STDIN": no kind "ClusterRole" is registered for version "rbac.authorization.k8s.io/v1"
