#!/bin/sh

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

. $DIR/env_bisrnn.sh

case $1 in
    create)
        gcloud dataproc clusters create ${CLUSTERNAME} --project $PROJECT --bucket $BUCKET --scopes=cloud-platform \
        --initialization-actions  gs://dataproc-initialization-actions/jupyter/jupyter.sh
        ;;
    ssh)
        # plain ssh as your current user !?
        echo "remember: PYSPARK_DRIVER_PYTHON=ipython pyspark"
        gcloud compute ssh "${CLUSTERNAME}-m" --project ${PROJECT} --zone=$ZONE
        ;;
    notebook)
        # or setup a tunnel and launch a notebook
        gcloud compute ssh "${CLUSTERNAME}-m" --project ${PROJECT} --zone=$ZONE -- -D 10000 -N -n &
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
            "http://${CLUSTERNAME}-m:8123" \
            --proxy-server="socks5://localhost:10000" \
            --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" \
            --user-data-dir=/tmp/
        ;;
    delete)
        gcloud dataproc clusters delete ${CLUSTERNAME}
        ;;
    *)
        echo "usage: dataproc.sh {create|ssh|notebook|delete}"
        exit 1
        ;;
esac
