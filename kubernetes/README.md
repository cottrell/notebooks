# ...

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