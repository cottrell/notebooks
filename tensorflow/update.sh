#!/bin/bash

case $1 in
    1gpu)
        pip install tf-nightly-gpu tb-nightly -U
        ;;
    2gpu)
        # tensorflow-estimator-2.0-preview
        pip install tf-nightly-gpu-2.0-preview tb-nightly -U
        ;;
    alpha)
        pip install tensorflow-gpu==2.0.0-alpha0 -u
        ;;
    *)
        echo prog 1gpu 2gpu
        ;;
esac