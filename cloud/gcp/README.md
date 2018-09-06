# google cloud workflow

For ml stuff use images as of 2018

    https://blog.kovalevskyi.com/deep-learning-images-for-google-cloud-engine-the-definitive-guide-bc74f5fb02bc

1. listing things (some things like disks are missing from the resource list in the UI)

	gsutil ls
	gcloud compute instances list
	gcloud dataproc clusters list
	gcloud compute disks list

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

# GPU

GCP ml-engine is a bit of a pain and I think still mainly focussed on tf. Avoid buying in too much for now.

ZONE europe-west1-b has v100: https://cloud.google.com/compute/docs/gpus/

You need to pick image names from this list: https://cloud.google.com/deep-learning-vm/docs/images

Or see google groups for bleeding edge availability: https://groups.google.com/forum/#!topic/google-dl-platform/Qsu2CVO0kV8

Probably just take a chance and pick the latest for now:

    tf-latest-cu92
    tf-latest-cpu
    pytorch-latest-cu92
    pytorch-latest-cpu

I do not know of a CLI command to get the list yet (`gcloud compute images list` does not show these for example).

Machines types:

    gcloud compute machine-types list --filter zone:europe-west1-b
        NAME             ZONE            CPUS  MEMORY_GB  DEPRECATED
    f1-micro         europe-west1-b  1     0.60
    g1-small         europe-west1-b  1     1.70
    n1-highcpu-16    europe-west1-b  16    14.40
    n1-highcpu-2     europe-west1-b  2     1.80
    n1-highcpu-32    europe-west1-b  32    28.80
    n1-highcpu-4     europe-west1-b  4     3.60
    n1-highcpu-64    europe-west1-b  64    57.60
    n1-highcpu-8     europe-west1-b  8     7.20
    n1-highcpu-96    europe-west1-b  96    86.40
    n1-highmem-16    europe-west1-b  16    104.00
    n1-highmem-2     europe-west1-b  2     13.00
    n1-highmem-32    europe-west1-b  32    208.00
    n1-highmem-4     europe-west1-b  4     26.00
    n1-highmem-64    europe-west1-b  64    416.00
    n1-highmem-8     europe-west1-b  8     52.00
    n1-highmem-96    europe-west1-b  96    624.00
    n1-megamem-96    europe-west1-b  96    1433.60
    n1-standard-1    europe-west1-b  1     3.75
    n1-standard-16   europe-west1-b  16    60.00
    n1-standard-2    europe-west1-b  2     7.50
    n1-standard-32   europe-west1-b  32    120.00
    n1-standard-4    europe-west1-b  4     15.00
    n1-standard-64   europe-west1-b  64    240.00
    n1-standard-8    europe-west1-b  8     30.00
    n1-standard-96   europe-west1-b  96    360.00
    n1-ultramem-160  europe-west1-b  160   3844.00
    n1-ultramem-40   europe-west1-b  40    961.00
    n1-ultramem-80   europe-west1-b  80    1922.00

See here for some info on picking zones, sizes, params etc: https://blog.kovalevskyi.com/deep-learning-images-for-google-cloud-engine-the-definitive-guide-bc74f5fb02bc
