# google cloud workflow

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
