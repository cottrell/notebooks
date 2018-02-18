# google cloud workflow

1. Buckets

	gsutil ls

1. Select or create a Cloud Platform project. Either go here: https://console.cloud.google.com/cloud-resource-manager or:

	gcloud projects list
	gcloud projects create <some name>

    	gcloud config list
	gcloud config set/get --project ...

    	gcloud config set compute/region europe-west1
    	gcloud config set compute/zone europe-west1-b
    	gcloud config set compute/region us-east1
    	gcloud compute zones list

	# look for BUCKET in env.sh ... probably not set dynamically.

1. Set up billing for project: https://console.cloud.google.com/billing/projects

1. Enable the Google Compute Engine and the Cloud Machine Learning APIs. (not working currently ... maybe not needed? gcloud just prompts you but is slow)

1. Set up gcloud for ml-engine

Create a new configuration with: `gcloud init`

	gcloud help config
	gcloud topic configurations

Activate with: `gcloud config configurations activate my-config`

See what models you have: `gcloud ml-engine models list`

1. Creating a Cloud Storage bucket

	BUCKET="misc-data-ml"
	gsutil mb -c regional -l europe-west1 gs://${BUCKET}
	gsutil cp all.text.gz gs://${BUCKET}/data/bis.text.gz

2. dataproc

	CLUSTERNAME=spark-cluster
	PROJECT=$(gcloud config list --format "value(core.project)")
	REGION=$(gcloud config list --format "value(compute.region)")
	ZONE=$(gcloud config list --format "value(compute.zone)")
	BUCKET=misc-data-ml
	gcloud dataproc clusters create ${CLUSTERNAME} --project $PROJECT --bucket $BUCKET --scopes=cloud-platform \
    		--initialization-actions  gs://dataproc-initialization-actions/jupyter/jupyter.sh

	# plain ssh as your current user !?
	gcloud compute ssh "${CLUSTERNAME}-m" --project ${PROJECT} --zone=$ZONE

	PYSPARK_DRIVER_PYTHON=ipython pyspark

	# or setup a tunnel and launch a notebook
	gcloud compute ssh "${CLUSTERNAME}-m" --project ${PROJECT} --zone=$ZONE -- -D 10000 -N
	# or add -n &

	/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    		"http://${CLUSTERNAME}-m:8123" \
    		--proxy-server="socks5://localhost:10000" \
    		--host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" \
    		--user-data-dir=/tmp/

	# delete
	gcloud dataproc clusters delete ${CLUSTERNAME}

	https://cloud.google.com/dataproc/docs/tutorials/jupyter-notebook

...

	gcloud compute ssh ${CLUSTERNAME}-m  --project project-id  --zone=cluster-zone -- -D 10000 -N

	gcloud dataproc clusters create ${CLUSTERNAME} --scopes=cloud-platform --tags codelab
  	# --zone=us-central1-c
	# Because you specified --scopes=cloud-platform when you created the cluster, you can run gcloud commands on your cluster. List the clusters in your project:

	gcloud dataproc jobs submit spark --cluster ${CLUSTERNAME} \
	--class org.apache.spark.examples.SparkPi --jars file:///usr/lib/spark/examples/jars/spark-examples.jar -- 1000

	gcloud dataproc jobs list --cluster ${CLUSTERNAME}
	gcloud dataproc jobs wait jobId
	gcloud dataproc clusters describe ${CLUSTERNAME}
	gcloud dataproc clusters update ${CLUSTERNAME} --num-preemptible-workers=2


	https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/init-actions

# dataflow

	conda create -n py27 python=2.7
	source activate py27
	enable a bunch of APIs as above
	pip install google-cloud-dataflow

