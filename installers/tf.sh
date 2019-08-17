# need to install nvidia 10 driver manually
source ./etc/profile.d/conda.sh
conda activate 37

if [[ $# -ne 1 ]]; then
    echo usage prog gpu cpu
fi

if [[ $1 = gpu ]]; then
    pip install tf-nightly-gpu-2.0-preview
elif [[ $1 = gpu ]]; then
    # pip install tf-nightly-2.0-preview
    pip install tensorflow==2.0.0-beta1
else
    echo unkown arg $1
    exit 1
fi

pip install -y tf-estimator-nightly tb-nightly tensorflow-estimator-2.0-preview

