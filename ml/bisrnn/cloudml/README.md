# google cloud workflow

Start here: https://cloud.google.com/ml-engine/docs/distributed-tensorflow-mnist-cloud-datalab

See here: cloudml-samples/census/keras

1. Select or create a Cloud Platform project. Either go here: https://console.cloud.google.com/cloud-resource-manager or:

	gcloud projects list
	gcloud projects create <some name>

2. Set up billing for project: https://console.cloud.google.com/billing/projects

3. Enable the Google Compute Engine and the Cloud Machine Learning APIs. (not working currently ... maybe not needed? gcloud just prompts you but is slow)

4. Set up gcloud

Create a new configuration with: `gcloud init`

	gcloud help config
	gcloud topic configurations

Activate with: `gcloud config configurations activate my-config`

See what models you have: `gcloud ml-engine models list`

5. Creating a Cloud Storage bucket

	# PROJECT_ID=$(gcloud config list project --format "value(core.project)")
	# BUCKET="${PROJECT_ID}-ml"
	BUCKET="misc-data-ml"
	# or use UI
	gsutil mb -c regional -l europe-west1 gs://${BUCKET}
	gsutil cp all.text.gz gs://${BUCKET}/data/bis.text.gz

6. Submit job

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
