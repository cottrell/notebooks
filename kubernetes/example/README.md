https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/
kubectl run hello-world --replicas=5 --labels="run=load-balancer-example" --image=gcr.io/google-samples/node-hello:1.0  --port=8080
kubectl describe deployments hello-world

or see minikube dash

kubectl expose deployment hello-world --type=LoadBalancer --name=my-service
kubectl get services my-service
kubectl describe services my-service

Might not work. Might need this

kubectl expose deployment microbot --port=80 --target-port=80 --type=NodePort


need to look at NodeBalancer Ingress, Port and NodePort

There is no "NodeBalancer Ingress" now. Something is wrong.


