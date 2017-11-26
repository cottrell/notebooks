# aws workflow

create s3 bucket: misc-data-ml-cottrell

	./put_data_s3.sh

# google cloud workflow

Start here: https://cloud.google.com/ml-engine/docs/distributed-tensorflow-mnist-cloud-datalab

See here: cloudml-samples/census/keras

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

	# PROJECT_ID=$(gcloud config list project --format "value(core.project)")
	# BUCKET="${PROJECT_ID}-ml"
	BUCKET="misc-data-ml"
	# or use UI
	gsutil mb -c regional -l europe-west1 gs://${BUCKET}
	gsutil cp all.text.gz gs://${BUCKET}/data/bis.text.gz

1. Submit job

	GO HERE: https://console.cloud.google.com/mlengine/jobs not easy to find from the project page.

	$ ./run.sh gcloud_mlengine
	method=gcloud_mlengine
	Job [job_20171028_143140] submitted successfully.
	Your job is still active. You may view the status of your job with the command

	  $ gcloud ml-engine jobs describe job_20171028_143140

	  or continue streaming the logs with the command

	    $ gcloud ml-engine jobs stream-logs job_20171028_143140
	    jobId: job_20171028_143140
	    state: QUEUED


	    Updates are available for some Cloud SDK components.  To install them,
	    please run:
	      $ gcloud components update

	other example:

	export JOB_NAME="job_$(date +%Y%m%d_%H%M%S)"
	gcloud ml-engine jobs submit training ${JOB_NAME} \
	    --package-path trainer \
	    --module-name trainer.task \
	    --staging-bucket gs://${BUCKET} \
	    --job-dir gs://${BUCKET}/${JOB_NAME} \
	    --runtime-version 1.2 \
	    --region us-central1 \
	    --config config/config.yaml \
	    -- \
	    --data_dir gs://${BUCKET}/data \
	    --output_dir gs://${BUCKET}/${JOB_NAME} \
	    --train_steps 10000
