tensorflow:

pip and vanilla installs requires manual installs of cuda drivers form nvda.


9.2 for old tf

sudo dpkg -i cuda-repo-ubuntu1710-9-2-local_9.2.148-1_amd64.deb
sudo apt-key add /var/cuda-repo-9-2-local/7fa2af80.pub
sudo apt-key add /var/cuda-repo-<version>/7fa2af80.pub
sudo apt-get update
sudo apt-get install cuda # 10
sudo apt-get install cuda-9.2

Or can install tf using conda for old tf.

For now tf (2.0) install cuda 10 and then via pip

> conda create -n tf2 python=3.6
> source activate tf2
> pip install tf-nightly-2.0-preview # tf-nightly-gpu-2.0-preview for GPU version

http://inoryy.com/post/tensorflow2-deep-reinforcement-learning/

but tfp will not work.

READ THIS: https://blog.kovalevskyi.com/multiple-version-of-cuda-libraries-on-the-same-machine-b9502d50ae77

