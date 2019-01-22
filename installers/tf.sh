conda create -n tf2gpu python=3.6
source activate tf2gpu
# need to install nvidia 10 driver manually
pip install tf-nightly-gpu-2.0-preview ipython


# another one tf 1
conda create -n tf python=3.6
pip install tf-nightly-gpu tfp-nightly

