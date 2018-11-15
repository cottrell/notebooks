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

