#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCE_GROUP=pach-resource-group
LOCATION="westeurope" # <a Azure availability zone where AKS is available, e.g, "Central US">
NODE_SIZE="Standard_DS4_v2" # <size for the k8s instances, we recommend at least "Standard_DS4_v2">
CLUSTER_NAME="pach-aks-cluster" # <unique name for the cluster, e.g., "pach-aks-cluster">
case $1 in
    create_cluster)
        # Create the Azure resource group.
        az group create --name=${RESOURCE_GROUP} --location="${LOCATION}"
        # Create the AKS cluster.
        az aks create --resource-group ${RESOURCE_GROUP} --name ${CLUSTER_NAME} --generate-ssh-keys --node-vm-size ${NODE_SIZE}
        ;;
    *)
        echo "do.sh deploy_k8ns"
        ;;
esac
