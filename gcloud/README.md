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

	see `dataproc.sh`

	This is very relevant https://cloud.google.com/dataproc/docs/tutorials/python-library-example

	https://cloud.google.com/dataproc/docs/tutorials/jupyter-notebook

	MISC
	gcloud dataproc clusters create ${CLUSTERNAME} --scopes=cloud-platform --tags codelab # --zone=us-central1-c
	# Because you specified --scopes=cloud-platform when you created the cluster, you can run gcloud commands on your cluster. List the clusters in your project:
	gcloud dataproc jobs submit spark --cluster ${CLUSTERNAME} \
	--class org.apache.spark.examples.SparkPi --jars file:///usr/lib/spark/examples/jars/spark-examples.jar -- 1000
	gcloud dataproc jobs list --cluster ${CLUSTERNAME}
	gcloud dataproc jobs wait jobId
	gcloud dataproc clusters describe ${CLUSTERNAME}
	gcloud dataproc clusters update ${CLUSTERNAME} --num-preemptible-workers=2

	https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/init-actions

# dataflow

	verdict: ugh, awful. try flink or nothing at all.

	conda create -n py27 python=2.7
	source activate py27
	enable a bunch of APIs as above
	pip install google-cloud-dataflow

