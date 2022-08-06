#!/bin/sh
# do this maybe: gcloud config set container/use_v1_api false
export DIR=/Users/davidcottrell/projects/notebooks/gcloud
export PROJECT=bisrnn
export REGION=europe-west1
export ZONE=europe-west1-b
export BUCKET=misc-data-ml
export BUCKET_NAME=$BUCKET
export CLUSTER_NAME="pach-cluster" # <any unique name, e.g. "pach-cluster">
export GCP_ZONE="europe-west1" # <a GCP availability zone. e.g. "us-west1-a">
export MACHINE_TYPE="n1-standard-4" # <machine type for the k8s nodes, we recommend "n1-standard-4" or larger>

STORAGE_SIZE=10 # <the size of the volume that you are going to create, in GBs. e.g. "10">

# troubleshooting:
#   kubectl get serviceaccounts
#   https://github.com/pachyderm/pachyderm/issues/2787
# $ kubectl delete clusterrolebinding pachyderm
# $ kubectl create clusterrolebinding pachyderm --clusterrole=cluster-admin --serviceaccount=pachyderm:pachyderm --namespace=pachyderm --user=system:serviceaccount:default:pachyderm
# $ kubectl delete pods --all
#   probably need to set IAM roles for cluster

case $1 in
    set)
        gcloud config set compute/zone ${GCP_ZONE}
        gcloud config set container/cluster ${CLUSTER_NAME}
        ;;
    delete_cluster)
        gcloud beta container clusters delete ${CLUSTER_NAME} 
        ;;
    create_cluster)
        # By default the following command spins up a 3-node cluster. You can change the default with `--num-nodes VAL`.
        gcloud config set compute/zone ${GCP_ZONE}
        gcloud config set container/cluster ${CLUSTER_NAME}
        gcloud config set container/use_v1_api false
        # gcloud container clusters create ${CLUSTER_NAME} --scopes storage-rw --machine-type ${MACHINE_TYPE}
        gcloud beta container clusters create ${CLUSTER_NAME} --scopes storage-rw --machine-type ${MACHINE_TYPE} --cluster-version "1.9.7-gke.0"
        # gcloud beta container --project "bisrnn" clusters create $CLUSTER_NAME --zone $GCP_ZONE --username "admin" --cluster-version "1.9.7-gke.0" --machine-type "n1-standard-1" --image-type "COS" --disk-size "100" --scopes "https://www.googleapis.com/auth/compute","https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "3" --network "default" --enable-cloud-logging --enable-cloud-monitoring --subnetwork "default" --addons HorizontalPodAutoscaling,HttpLoadBalancing,KubernetesDashboard --enable-autorepair
        ;;
    get_pods)
        kubectl get pods -n kube-system
        ;;
    update_cred)
        # Update your kubeconfig to point at your newly created cluster.
        gcloud beta container clusters get-credentials ${CLUSTER_NAME}
        ;;
    create_storage)
        echo not needed now
        # For the persistent disk, 10GB is a good size to start with.
        # This stores PFS metadata. For reference, 1GB
        # should work fine for 1000 commits on 1000 files.
        # The Pachyderm bucket name needs to be globally unique across the entire GCP region.
        # $ BUCKET_NAME=<The name of the GCS bucket where your data will be stored>
        # # Create the bucket.
        # $ gsutil mb gs://${BUCKET_NAME}
        ;;
    deploy)
        pachctl deploy google ${BUCKET_NAME} ${STORAGE_SIZE} --dynamic-etcd-nodes=1
        # kubectl get all
        # pachctl port-forward
esac
