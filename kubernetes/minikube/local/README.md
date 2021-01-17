# notes

    google cloud sdk puts kubectl in the path. this is bad. Check what you are using first!

    brew info kubectl
    type kubectl

    export PATH=/usr/local/Cellar/kubernetes-cli/1.11.2/bin:$PATH

    Do some install on Docker app itself.

    Can use minikube or docker for desktop? DO NOT USE MINIKUBE FOR NOW!

    $ kubectl config get-contexts
    CURRENT   NAME                 CLUSTER                      AUTHINFO             NAMESPACE
    docker-for-desktop   docker-for-desktop-cluster   docker-for-desktop
    *         minikube             minikube                     minikube

    kubectl config current-context
    kubectl config use-context docker-for-desktop

    kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
    kubectl get all --all-namespaces
    kubectl get pods --namespace=kube-system
    kubectl port-forward kubernetes-dashboard-7d5dcdb6d9-grxsw 8443:8443 --namespace=kube-system

    host might be 10.0.0.2 from virtuabox???

# example (run some image with a command)

Without creating Dockerfile

    # kubectl run ubuntu -n default --image ubuntu:latest --command /bin/bash
    kubectl run u --rm -i --tty --image ubuntu:latest -- bash
    kubectl run u --rm -i --tty --image centos_postgres -- bash

# example (nginx)

    kubectl run hello-nginx --image=nginx --port=80
    kubectl get pods
    kubectl get deployments
    kubectl expose deployment hello-nginx --type=NodePort
    kubectl describe service hello-nginx

# example (metabase)

    also see notebooks/metabase/run.sh
    docker pull metabase/metabase
    kubectl expose deployment metabase-example --type=NodePort (no you probably want LoadBalancer)





    # OLD IGNORE
    minikube start
    kubectl version
    kubectl cluster-info

    kubectl get nodes
    kubectl run kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1 --port=8080
    kubectl get deployments
    kubectl proxy
    curl http://localhost:8001/version
    export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
    echo Name of the Pod: $POD_NAME
    curl http://localhost:8001/api/v1/proxy/namespaces/default/pods/$POD_NAME/

    kubectl get pods
    kubectl describe pods

    kubectl get services
    kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
    kubectl describe services/kubernetes-bootcamp
    export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
    echo NODE_PORT=$NODE_PORT
    curl $(minikube ip):$NODE_PORT

    # labels
    kubectl describe deployment
    kubectl get pods -l run=kubernetes-bootcamp
    kubectl get services -l run=kubernetes-bootcamp
    export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
    echo Name of the Pod: $POD_NAME
    kubectl label pod $POD_NAME app=v1
    kubectl describe pods $POD_NAME
    kubectl get pods -l app=v1

    kubectl delete service -l run=kubernetes-bootcamp
    curl $(minikube ip):$NODE_PORT # run outside to show it is off
    kubectl exec -ti $POD_NAME curl localhost:8080 # run inside pod

    # scaling
    kubectl get deployments
    kubectl scale deployments/kubernetes-bootcamp --replicas=4
    kubectl get pods -o wide
    kubectl describe deployments/kubernetes-bootcamp # check the log for deployment events

    export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
    echo NODE_PORT=$NODE_PORT
    curl $(minikube ip):$NODE_PORT # curling multiple times gets different pod

    # scale down
    kubectl scale deployments/kubernetes-bootcamp --replicas=2
