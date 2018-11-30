# Current State:

    mnist.py segfaults
    mnist2.py ok

https://www.pugetsystems.com/labs/hpc/Install-TensorFlow-with-GPU-Support-the-Easy-Way-on-Ubuntu-18-04-without-installing-CUDA-1170/

Removed CUDA. Now mnist2.py seems to run but mnist.py still segfaults when run interactively.


$ date
Fri 30 Nov 18:43:29 GMT 2018
$ python check_gpu.py
2018-11-30 18:43:06.421660: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA
2018-11-30 18:43:06.517961: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:964] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2018-11-30 18:43:06.518440: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1432] Found device 0 with properties:
name: GeForce RTX 2070 major: 7 minor: 5 memoryClockRate(GHz): 1.62
pciBusID: 0000:01:00.0
totalMemory: 7.76GiB freeMemory: 6.32GiB
2018-11-30 18:43:06.518452: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2018-11-30 18:43:06.882676: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2018-11-30 18:43:06.882701: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
2018-11-30 18:43:06.882706: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
2018-11-30 18:43:06.882976: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/device:GPU:0 with 6075 MB memory) -> physical GPU (device: 0, name: GeForce RTX 2070, pci bus id: 0000:01:00.0, compute capability: 7.5)
cuda_only=False True

2018-11-30 18:43:06.883874: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2018-11-30 18:43:06.883892: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2018-11-30 18:43:06.883899: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
2018-11-30 18:43:06.883904: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
2018-11-30 18:43:06.884134: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/device:GPU:0 with 6075 MB memory) -> physical GPU (device: 0, name: GeForce RTX 2070, pci bus id: 0000:01:00.0, compute capability: 7.5)
cuda_only=True True
