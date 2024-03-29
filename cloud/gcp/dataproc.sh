#!/bin/sh

ME_SHORT=${BASH_SOURCE[0]}
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ME=$DIR/$(basename ${BASH_SOURCE[0]})

. $DIR/env_bisrnn.sh

case $1 in
    vanilla)
        # for debug of init actions for example
        gcloud dataproc clusters create ${CLUSTERNAME} --project $PROJECT --bucket $BUCKET --zone $ZONE
        ;;
    create)
        # --scopes=cloud-platform \
        gcloud dataproc clusters create ${CLUSTERNAME} --project $PROJECT --bucket $BUCKET --initialization-actions gs://misc-data-ml/init_action.sh \
        --num-preemptible-workers 3 --num-workers 3 --zone $ZONE
        # --initialization-actions gs://dataproc-initialization-actions/jupyter/jupyter.sh
        ;;
    list)
        gcloud dataproc clusters list
        ;;
    ssh)
        # plain ssh as your current user !?
        echo "remember: PYSPARK_DRIVER_PYTHON=ipython pyspark"
        gcloud compute ssh "${CLUSTERNAME}-m" --project ${PROJECT} --zone=$ZONE
        ;;
    ui)
        gcloud compute ssh "${CLUSTERNAME}-m" --project ${PROJECT} --zone=$ZONE -- -D 10000 -N -n &
        mkdir -p /tmp/master-host-name
        for port in 8088 9870 8123; do
            /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
                "http://${CLUSTERNAME}-m:$port" \
                --proxy-server="socks5://localhost:10000" \
                --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" \
                --user-data-dir=/tmp/ &
        done
        ;;
    notebook)
        gcloud compute ssh "${CLUSTERNAME}-m" --project ${PROJECT} --zone=$ZONE -- -D 10000 -N -n &
        # or setup a tunnel and launch a notebook
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
            "http://${CLUSTERNAME}-m:8123" \
            --proxy-server="socks5://localhost:10000" \
            --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" \
            --user-data-dir=/tmp/
        ;;
    delete)
        gcloud dataproc clusters delete ${CLUSTERNAME}
        ;;
    listjobs)
        gcloud dataproc jobs list --cluster ${CLUSTERNAME}
        ;;
    describe)
        gcloud dataproc clusters describe ${CLUSTERNAME}
        ;;
    update)
        if [[ ! "$2" ]]; then
            echo update num
            exit
        fi
        echo updating to $2 workers
        gcloud dataproc clusters update ${CLUSTERNAME} --num-workers=$2
        ;;
    updatepreemptible)
        if [[ ! "$2" ]]; then
            echo update num
            exit
        fi
        echo updating to $2 preemptible workers
        gcloud dataproc clusters update ${CLUSTERNAME} --num-preemptible-workers=$2
        ;;
    *)
        # echo "usage: dataproc.sh {create|ssh|notebook|delete}"
        echo usage: $ME_SHORT $(cat $ME | awk '/^case .* in$/{flag=1;next}/^esac/{flag=0}flag' | sed -n 's/^ *\([^\s]*\))/\1/p' | grep -v '*' | paste -sd '|' -)
        exit 1
        ;;
esac
