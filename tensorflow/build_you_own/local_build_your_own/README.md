# links

* https://medium.com/@Oysiyl/install-tensorflow-1-8-0-with-gpu-from-source-on-ubuntu-18-04-bionic-beaver-35cfa9df3600
* https://www.pugetsystems.com/labs/hpc/How-to-install-CUDA-9-2-on-Ubuntu-18-04-1184/


# check nvidia driver
	nvidia-smi

	./cuda_9.2.148_396.37_linux.run --override # do not say yes to the Driver part.
	sudo ./cuda_9.2.148.1_linux.run

	===========
	= Summary =
	===========

	Driver:   Not Selected
	Toolkit:  Installed in /usr/local/cuda-9.2
	Samples:  Installed in /home/cottrell

	Please make sure that
	 -   PATH includes /usr/local/cuda-9.2/bin
	 -   LD_LIBRARY_PATH includes /usr/local/cuda-9.2/lib64, or, add /usr/local/cuda-9.2/lib64 to /etc/ld.so.conf and run ldconfig as root

	To uninstall the CUDA Toolkit, run the uninstall script in /usr/local/cuda-9.2/bin

	Please see CUDA_Installation_Guide_Linux.pdf in /usr/local/cuda-9.2/doc/pdf for detailed information on setting up CUDA.

	# Unpack the archive
	tar -zxvf cudnn-9.2-linux-x64-v7.4.1.5.tgz
	# Move the unpacked contents to your CUDA directory
	sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda-9.2/lib64/
	sudo cp  cuda/include/cudnn.h /usr/local/cuda-9.2/include/
	# Give read access to all users
	# sudo chmod a+r /usr/local/cuda-9.2/include/cudnn.h /usr/local/cuda-9.2/lib64/libcudnn*

	tar -xvf nccl_2.3.7-1+cuda9.2_x86_64.txz
	sudo cp ./nccl_2.3.7-1+cuda9.2_x86_64/lib/* /usr/local/cuda-9.2/lib64/
	sudo cp ./nccl_2.3.7-1+cuda9.2_x86_64/include/* /usr/local/cuda-9.2/include/

	sudo apt-get install libcupti-dev
	echo 'export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc

	sudo chmod a+r -R /usr/local/cuda-9.2

	# then build tensorflow

	./configure

	# you get compute capacity from some tool command in /usr/local/cuda-9.2/samples which takes a while to build. I think answer is 7.5

	# need some old gcc ... check the tables
	sudo apt-get install gcc-4.8
	sudo apt-get install -y g++-4.8
	# also look at cc1plus ... some error comes up later


	use the base flags for now, but you probably want mkl option later.

	bazel build --config=opt --config=cuda //tensorflow/tools/pip_package:build_pip_package # fails
	# this seems to  get it farther:
	BAZEL_SH=/usr/local/bin/bazel PYTHON_LIB_PATH=~/anaconda3/envs/36/lib PYTHON_BIN_PATH=~/anaconda3/envs/36/bin/ bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package

	# YOU NEED THE CUDA SAMPLES, /usr/local/cuda-9.2/sample ... they are built with : make -k


	# TODO put this in a docker image
