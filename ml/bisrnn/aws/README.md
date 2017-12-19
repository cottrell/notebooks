# notes

https://aws.amazon.com/blogs/aws/new-amazon-ec2-instances-with-up-to-8-nvidia-tesla-v100-gpus-p3/

For ad hoc stuff, for example if you want a notebook, just do ec2.

setup security rule. add custom access for ssh and for tcp port 8888. use your ip.

Make sure to log in as ubuntu

	ssh -i "~/.cred/aws/2017kp.pem" ubuntu@ec2-54-171-60-94.eu-west-1.compute.amazonaws.com

	aws configure # set up credentials, needed for boto3

	jupyter notebook --ip=0.0.0.0 --no-browser

	conda install bcolz
	pip install argh
	# check gpu maybe

	. ./env.sh
	ipython

	In [4]: import tensorflow as tf
   	...: sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
   	...:
	2017-11-27 20:35:45.406258: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA
	2017-11-27 20:35:46.791969: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:892] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
	2017-11-27 20:35:46.792319: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Found device 0 with properties:
	name: Tesla K80 major: 3 minor: 7 memoryClockRate(GHz): 0.8235
	pciBusID: 0000:00:1e.0
	totalMemory: 11.17GiB freeMemory: 11.10GiB
	2017-11-27 20:35:46.792350: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1120] Creating TensorFlow device (/device:GPU:0) -> (device: 0, name: Tesla K80, pci bus id: 0000:00:1e.0, compute capability: 3.7)
	Device mapping:
	/job:localhost/replica:0/task:0/device:GPU:0 -> device: 0, name: Tesla K80, pci bus id: 0000:00:1e.0, compute capability: 3.7
	2017-11-27 20:35:46.902337: I tensorflow/core/common_runtime/direct_session.cc:299] Device mapping:
	/job:localhost/replica:0/task:0/device:GPU:0 -> device: 0, name: Tesla K80, pci bus id: 0000:00:1e.0, compute capability: 3.7

# more from feedback/help from aws

	http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html

	http://docs.aws.amazon.com/cli/latest/userguide/cli-ec2-launch.html#listing-instances

	https://console.aws.amazon.com/billing/home#/bill

	https://console.aws.amazon.com/console/home?region=us-east-1

