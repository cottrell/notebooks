#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PROJECT=$(gcloud config list --format "value(core.project)")
REGION=$(gcloud config list --format "value(compute.region)")
ZONE=$(gcloud config list --format "value(compute.zone)")
BUCKET=misc-data-ml
CLUSTERNAME=spark-cluster

for x in $(grep '^[A-Z]*=' $DIR/env.sh | grep -v '^DIR' | cut -d'=' -f1); do echo export $x=${!x}; done > $DIR/env_$PROJECT.sh

echo see $DIR/env_$PROJECT.sh
