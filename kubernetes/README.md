# quickstart

    # install virtual box
    sudo apt-get install virtualbox virtualbox-ext-pack
    # install minikube
    minikube start

    # install kubectl

    # check kubectl
    kubectl cluster-info

    kubectl config use-context
    kubectl cluster-info dump
    The connection to the server localhost:8080 was refused - did you specify the right host or port?



    # install minikube
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64   && chmod +x minikube
    sudo cp minikube /usr/local/bin && rm minikube


minikube start


# cloud

A good place to start: https://zero-to-jupyterhub.readthedocs.io

There is Helm. https://helm.sh/ I do not know why I did not see this before.

    curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash


## gcp

gcloud components install kubectl

gcloud container clusters create <YOUR_CLUSTER> \
    --num-nodes=3 \
    --machine-type=n1-standard-2 \
    --zone=us-central1-b

# local

See './local'

