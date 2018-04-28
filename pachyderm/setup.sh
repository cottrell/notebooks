#!/bin/sh
# had to force the link to update it
# brew install kubectl
# brew link --overwrite kubernetes-cli
minikube stop
minikube delete
minikube start
if [ "$(uname)" = "Darwin" ]; then
    brew tap pachyderm/tap && brew install pachyderm/tap/pachctl@1.7
else
    curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v1.7.1/pachctl_1.7.1_amd64.deb && sudo dpkg -i /tmp/pachctl.deb
fi
pachctl deploy local
kubectl get pods
pachctl port-forward &

# get errors unable to decode "STDIN": no kind "ClusterRole" is registered for version "rbac.authorization.k8s.io/v1"
