# Try this?

https://www.tensorflow.org/install/gpu

purge all and install the correct driver ! 410 see ubuntu/nvidia_purge.sh and cuda_purge.sh

# As of 2019-03

    STILL NOT WORKING WAS WRONG

    ##########################################
    ##########################################
    ## nvidia-410 and CUDA 10-0 CUDNN 7.4.2 ##
    ## nvidia-410 and CUDA 10-0 CUDNN 7.4.2 ##
    ## nvidia-410 and CUDA 10-0 CUDNN 7.4.2 ##
    ## nvidia-410 and CUDA 10-0 CUDNN 7.4.2 ##
    ## nvidia-410 and CUDA 10-0 CUDNN 7.4.2 ##
    ## nvidia-410 and CUDA 10-0 CUDNN 7.4.2 ##
    ##########################################
    ##########################################

Later version of nvidia drivers seem to be ok across the board for tf-nightly-gpu and tf 2.0.

Do a clean install/purge of nvidia (mostly cuda) and cuda (see ../ubuntu notes one level up).

Download latest nvidia cuda driver manually and follow the instructions there that usually look something like this:

    sudo dpkg -i ./cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb
    sudo apt-key add /var/cuda-repo-10-0-local-10.0.130-410.48/7fa2af80.pub
    sudo apt-get update
    sudo apt-get install cuda-10-0

    $ cat ~/.bashrc | grep cuda
    # not sure need these unless doing cuda dev
    # # set PATH for cuda installation
    if [ -d "/usr/local/cuda/bin/" ]; then
        export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
        export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
        export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH
    fi
    nvcc --version
    $ nvcc --version
        nvcc: NVIDIA (R) Cuda compiler driver
        Copyright (c) 2005-2018 NVIDIA Corporation
        Built on Sat_Aug_25_21:08:01_CDT_2018
        Cuda compilation tools, release 10.0, V10.0.130

Then cudnn another manual download that requires login to nvidia. Make sure you GET THE LATEST NOT THE ARCHIVE.

    # NOT 7.5!
    sudo dpkg -i ./libcudnn7_7.4.2.24-1+cuda10.0_amd64.deb

Remember the cudnn problems do not become apparent until you try conv etc.

And it goes on. Something to do with allow_growth:

    from keras.backend.tensorflow_backend import set_session
    from tensorflow.compat.v1 import ConfigProto
    from tensorflow.compat.v1 import InteractiveSession, Session
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    config.log_device_placement = True  # to log device placement (on which device the operation ran)
    # session = InteractiveSession(config=config)
    import tensorflow as tf
    session = tf.Session(config=config)
    set_session(session)  # set this TensorFlow session as the default session for Keras

