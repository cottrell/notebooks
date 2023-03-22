# 2023-03-22

python 3.11 ... jax seems to require later version of nvidia.  https://github.com/google/jax/issues/14480 ... cuda 11.8 nvidia 520.61 ... will take some time. Do this later.

Going to run through the procedure below purging first.

Had to do this fix https://askubuntu.com/questions/1436601/ubuntu-drivers-unboundlocalerror-local-variable-version-referenced-before-as

    ./cuda_purge.sh
    ./nvidia_purge.sh
    sudo apt-get update
    $ ubuntu-drivers devices
    ...
    sudo ubuntu-drivers autoinstall
    sudo apt install nvidia-cuda-toolkit
    sudo apt-get update
    reboot

    $ ubuntu-drivers devices
    == /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
    modalias : pci:v000010DEd00001F02sv000019DAsd00002516bc03sc00i00
    vendor   : NVIDIA Corporation
    model    : TU106 [GeForce RTX 2070]
    manual_install: True
    driver   : nvidia-driver-525-server - distro non-free
    driver   : nvidia-driver-510 - distro non-free
    driver   : nvidia-driver-470-server - distro non-free
    driver   : nvidia-driver-515 - distro non-free
    driver   : nvidia-driver-470 - distro non-free
    driver   : nvidia-driver-525 - distro non-free
    driver   : nvidia-driver-418-server - distro non-free
    driver   : nvidia-driver-515-open - distro non-free
    driver   : nvidia-driver-450-server - distro non-free
    driver   : nvidia-driver-515-server - distro non-free
    driver   : nvidia-driver-525-open - distro non-free recommended
    driver   : xserver-xorg-video-nouveau - distro free builtin

    jax test in 3.10.4 now fails to find GPU
    nvidia-smi does not exist

    sudo apt install nvidia-cuda-toolkit
    ... still nope ... I need to do this I think
    ./nvidia_purge.sh
    sudo apt install nvidia-utils-525
    reboot
    $ nvidia-smi
    NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.
    sudo apt install nvidia-cuda-toolkit
    nvidia-smi no longer found
    jax passes but on cpu on both versions now

    ./cuda_purge.sh
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt-get update
    sudo apt-get -y install cuda




# 2022-07-13

When I run jax/check_gpu.py:

    kernel version 515.48.7 does not match DSO version 510.73.5 -- cannot find working devices in this configuration


Going to try to purge nvidia and cudo and reinstall and reboot https://forums.developer.nvidia.com/t/kernel-version-440-31-0-does-not-match-dso-version-440-33-1-mdash-cannot-find-working-devices-in-this-configuration/107975:

    ./cuda_purge.sh
    ./nvidia_purge.sh
    sudo apt-get update
    $ ubuntu-drivers devices
    == /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
    modalias : pci:v000010DEd00001F02sv000019DAsd00002516bc03sc00i00
    vendor   : NVIDIA Corporation
    model    : TU106 [GeForce RTX 2070]
    driver   : nvidia-driver-470-server - distro non-free
    driver   : nvidia-driver-510-server - distro non-free
    driver   : nvidia-driver-515 - distro non-free recommended
    driver   : nvidia-driver-470 - distro non-free
    driver   : nvidia-driver-510 - distro non-free
    driver   : nvidia-driver-418-server - distro non-free
    driver   : nvidia-driver-515-server - distro non-free
    driver   : nvidia-driver-450-server - distro non-free
    driver   : xserver-xorg-video-nouveau - distro free builtin

    sudo ubuntu-drivers autoinstall
    sudo apt install nvidia-cuda-toolkit
    sudo apt-get update
    reboot
    still same thing not working

    ./nvidia_purge.sh
    sudo apt-get install nvidia-utils-510

    reboot
    still does not work
    now screen res is not correct

    Arg ... should have done: sudo apt install nvidia-driver-510 ... (not utils)
    ./nvidia_purge.sh
    sudo apt install nvidia-driver-510
    reboot

    now get core dump on check_gpu.py
    sudo apt-get update
    ./cuda_purge.sh
    sudo apt install nvidia-cuda-toolkit
    NOW WORKS! Without reboot. Going to reboot to make sure nothing else is busted.
    reboot
    works!






# 2022-07-12

Noticed jax not working again.

nvidia-smi works but ./check_gpu.py fails.

    $ TF_CPP_MIN_LOG_LEVEL=0 ./check_gpu.py
    2022-07-12 15:43:36.311703: I external/org_tensorflow/tensorflow/compiler/xla/service/service.cc:172] XLA service 0x562cb9ff4800 initialized for platform Interpreter (this does not guarantee that XLA will be used). Devices:
    2022-07-12 15:43:36.311723: I external/org_tensorflow/tensorflow/compiler/xla/service/service.cc:180]   StreamExecutor device (0): Interpreter, <undefined>
    2022-07-12 15:43:36.313854: I external/org_tensorflow/tensorflow/compiler/xla/pjrt/tfrt_cpu_pjrt_client.cc:181] TfrtCpuClient created.
    2022-07-12 15:43:36.314173: I external/org_tensorflow/tensorflow/core/tpu/tpu_initializer_helper.cc:262] Libtpu path is: libtpu.so
    2022-07-12 15:43:36.314403: I external/org_tensorflow/tensorflow/stream_executor/tpu/tpu_platform_interface.cc:74] No TPU platform found.
    WARNING:absl:No GPU/TPU found, falling back to CPU. (Set TF_CPP_MIN_LOG_LEVEL=0 and rerun for more info.)
    cpu


    $ nvidia-smi
    Tue Jul 12 15:41:40 2022
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 510.73.05    Driver Version: 510.73.05    CUDA Version: 11.6     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0  On |                  N/A |
    | 30%   43C    P8    17W / 175W |    827MiB /  8192MiB |     11%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |    0   N/A  N/A      3384      G   /usr/lib/xorg/Xorg                297MiB |
    |    0   N/A  N/A      3533      G   /usr/bin/gnome-shell              119MiB |
    |    0   N/A  N/A      4361      G   ...RendererForSitePerProcess       11MiB |
    |    0   N/A  N/A   2629083      G   ...861081016357593163,131072      395MiB |
    +-----------------------------------------------------------------------------+

Trying:

    sudo ubuntu-drivers autoinstall


Does not work.

... various problems. resolved.

gpu still not work.

    nvidia-smi
    Tue Jul 12 17:30:54 2022
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 515.48.07    Driver Version: 515.48.07    CUDA Version: 11.7     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0  On |                  N/A |
    | 30%   44C    P8    16W / 175W |   1936MiB /  8192MiB |      4%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |    0   N/A  N/A      3160      G   /usr/lib/xorg/Xorg                183MiB |
    |    0   N/A  N/A      3307      G   /usr/bin/gnome-shell               63MiB |
    |    0   N/A  N/A      3956      G   ...364554119117281805,131072     1686MiB |
    +-----------------------------------------------------------------------------+


Now try:

        sudo apt install nvidia-cuda-toolkit


Still fails. Also tensorflow fails.

Reboot.

Reinstall jax as per README

    sudo ubuntu-drivers autoinstall


Now have: Couldn't get ptxas version string: INTERNAL: Couldn't invoke ptxas --version


    sudo apt install nvidia-cuda-toolkit


I maybe need to downgarde to 510?


# 2022-05-26

Noticed jax not working. Made the check_gpu.py script repro the error now.

Error says something about "Couldn't invoke ptxas --version"

Trying:

    sudo apt install nvidia-cuda-toolkit

Ok, now check_gpu.py runs but CPU only.

Going to try reboot.

Still only cpu.

    $ uname -sr
    Linux 5.15.0-33-generic

    $ lsb_release -a
    No LSB modules are available.
    Distributor ID:	Ubuntu
    Description:	Ubuntu 22.04 LTS
    Release:	22.04
    Codename:	jammy

Jax check shows: CUDA_ERROR_COMPAT_NOT_SUPPORTED_ON_DEVICE

huh ... nvidia-smi not found.

Following: https://www.linuxcapable.com/how-to-install-nvidia-drivers-on-ubuntu-22-04-lts/

    ubuntu-drivers devices
    == /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
    modalias : pci:v000010DEd00001F02sv000019DAsd00002516bc03sc00i00
    vendor   : NVIDIA Corporation
    model    : TU106 [GeForce RTX 2070]
    driver   : nvidia-driver-470 - distro non-free
    driver   : nvidia-driver-510 - distro non-free recommended
    driver   : nvidia-driver-418-server - distro non-free
    driver   : nvidia-driver-510-server - distro non-free
    driver   : nvidia-driver-470-server - distro non-free
    driver   : nvidia-driver-450-server - distro non-free
    driver   : xserver-xorg-video-nouveau - distro free builtin


Ok ... let's go with recommended:


    sudo ubuntu-drivers autoinstall


Reboot.

    nvidia-smi
    Thu May 26 19:20:26 2022
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 510.73.05    Driver Version: 510.73.05    CUDA Version: 11.6     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0  On |                  N/A |
    | 30%   40C    P8    18W / 175W |    169MiB /  8192MiB |      4%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |    0   N/A  N/A      3268      G   /usr/lib/xorg/Xorg                 86MiB |
    |    0   N/A  N/A      3381      G   ...ome-remote-desktop-daemon        1MiB |
    |    0   N/A  N/A      3417      G   /usr/bin/gnome-shell               78MiB |
    +-----------------------------------------------------------------------------+


jax/check_gpu.py now passes.


# 2022-01-14

After upgrade. Jax check_gpu.py failing. nvidia-smi ok.


This fixed it:

    sudo apt install nvidia-cuda-toolkit


tf gpu check passing.


# 2021-08-04 minor update failure event

nvidia-smi was failing after some auto-update

reboot fixed it

check_gpu.py passing again.

# 2021-02-21 nvidia driver reinstall

Awful.


    uname -sr
    Linux 5.4.0-65-generic

    lsb_release -a
    No LSB modules are available.
    Distributor ID:	Ubuntu
    Description:	Ubuntu 20.04.2 LTS
    Release:	20.04
    Codename:	focal

After many attempts this finally seemed to work to at least bring back the monitor resolution etc: https://askubuntu.com/questions/1310433/nvidia-driver-460-does-not-work-with-5-4-0-64-kernel-in-ubuntu-18-04

Tensorflow is not yet detecting the GPU but that is probably because I haven't done CUDA yet. See below for when I try that again.

Always check the dpkg command below. I think the issue is something to do with the kernel headers or the nvidia-settings version always being 460.

The steps are precisely (I am not sure if downgrading gcc is strictly necessary):

    ./nvidia_purge.sh
    sudo apt install gcc-8
    sudo update-alternatives --remove-all gcc
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 10
    sudo update-alternatives --install /usr/bin/cc cc /usr/bin/gcc-8 10
    sudo apt-get install --reinstall linux-headers-$(uname -r)
    sudo apt-get install nvidia-driver-460
    # reboot

    dpkg --list | grep nvidia
    ii  libnvidia-cfg1-460:amd64                      460.32.03-0ubuntu1                          amd64        NVIDIA binary OpenGL/GLX configuration library
    ii  libnvidia-common-460                          460.32.03-0ubuntu1                          all          Shared files used by the NVIDIA libraries
    ii  libnvidia-compute-460:amd64                   460.32.03-0ubuntu1                          amd64        NVIDIA libcompute package
    ii  libnvidia-decode-460:amd64                    460.32.03-0ubuntu1                          amd64        NVIDIA Video Decoding runtime libraries
    ii  libnvidia-encode-460:amd64                    460.32.03-0ubuntu1                          amd64        NVENC Video Encoding runtime library
    ii  libnvidia-extra-460:amd64                     460.32.03-0ubuntu1                          amd64        Extra libraries for the NVIDIA driver
    ii  libnvidia-fbc1-460:amd64                      460.32.03-0ubuntu1                          amd64        NVIDIA OpenGL-based Framebuffer Capture runtime library
    ii  libnvidia-gl-460:amd64                        460.32.03-0ubuntu1                          amd64        NVIDIA OpenGL/GLX/EGL/GLES GLVND libraries and Vulkan ICD
    ii  libnvidia-ifr1-460:amd64                      460.32.03-0ubuntu1                          amd64        NVIDIA OpenGL-based Inband Frame Readback runtime library
    ii  nvidia-compute-utils-460                      460.32.03-0ubuntu1                          amd64        NVIDIA compute utilities
    ii  nvidia-dkms-460                               460.32.03-0ubuntu1                          amd64        NVIDIA DKMS package
    ii  nvidia-driver-460                             460.32.03-0ubuntu1                          amd64        NVIDIA driver metapackage
    ii  nvidia-kernel-common-460                      460.32.03-0ubuntu1                          amd64        Shared files used with the kernel module
    ii  nvidia-kernel-source-460                      460.32.03-0ubuntu1                          amd64        NVIDIA kernel source package
    ii  nvidia-prime                                  0.8.15.3~0.20.04.1                          all          Tools to enable NVIDIA's Prime
    ii  nvidia-settings                               460.32.03-0ubuntu1                          amd64        Tool for configuring the NVIDIA graphics driver
    ii  nvidia-utils-460                              460.32.03-0ubuntu1                          amd64        NVIDIA driver support binaries
    ii  screen-resolution-extra                       0.18build1                                  all          Extension for the nvidia-settings control panel
    ii  xserver-xorg-video-nvidia-460                 460.32.03-0ubuntu1                          amd64        NVIDIA binary Xorg driver

    nvidia-smi
    Sun Feb 21 12:56:51 2021
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 460.32.03    Driver Version: 460.32.03    CUDA Version: 11.2     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  GeForce RTX 2070    On   | 00000000:01:00.0  On |                  N/A |
    | 36%   44C    P8     9W / 175W |    373MiB /  7979MiB |      2%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |    0   N/A  N/A      1930      G   /usr/lib/xorg/Xorg                 35MiB |
    |    0   N/A  N/A      3595      G   /usr/lib/xorg/Xorg                176MiB |
    |    0   N/A  N/A      3724      G   /usr/bin/gnome-shell               82MiB |
    |    0   N/A  N/A      4421      G   ...AAAAAAAA== --shared-files       67MiB |
    +-----------------------------------------------------------------------------+

Remember the following:

Run purge between any attempts

    ./nvidia_purge.sh
    ./cuda_purge.sh

Always check this, something to do with secure boot?

    dpkg --list | grep ii.*nvidia

## Checks and tests

	sudo lspci -v
	01:00.0 VGA compatible controller: NVIDIA Corporation TU106 [GeForce RTX 2070] (rev a1) (prog-if 00 [VGA controller])
    Subsystem: ZOTAC International (MCO) Ltd. TU106 [GeForce RTX 2070]
    Flags: bus master, fast devsel, latency 0, IRQ 11
    Memory at de000000 (32-bit, non-prefetchable) [size=16M]
    Memory at c0000000 (64-bit, prefetchable) [size=256M]
    Memory at d0000000 (64-bit, prefetchable) [size=32M]
    I/O ports at e000 [size=128]
    Expansion ROM at 000c0000 [disabled] [size=128K]
    Capabilities: [60] Power Management version 3
    Capabilities: [68] MSI: Enable- Count=1/1 Maskable- 64bit+
    Capabilities: [78] Express Legacy Endpoint, MSI 00
    Capabilities: [100] Virtual Channel
    Capabilities: [250] Latency Tolerance Reporting
    Capabilities: [258] L1 PM Substates
    Capabilities: [128] Power Budgeting <?>
    Capabilities: [420] Advanced Error Reporting
    Capabilities: [600] Vendor Specific Information: ID=0001 Rev=1 Len=024 <?>
    Capabilities: [900] Secondary PCI Express
    Capabilities: [bb0] Resizable BAR <?>
    Kernel modules: nvidiafb, nouveau

	nvidia-smi -a
	NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.

    sudo ubuntu-drivers devices
    == /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
    modalias : pci:v000010DEd00001F02sv000019DAsd00002516bc03sc00i00
    vendor   : NVIDIA Corporation
    model    : TU106 [GeForce RTX 2070]
    driver   : nvidia-driver-450 - third-party non-free
    driver   : nvidia-driver-450-server - distro non-free
    driver   : nvidia-driver-460 - third-party non-free recommended
    driver   : nvidia-driver-418-server - distro non-free
    driver   : xserver-xorg-video-nouveau - distro free builtin


## 2021-02-21 Cuda and Tensorflow

See requirements at https://www.tensorflow.org/install/gpu but basically you can just go the nvidia and use their install scripts. Then test and see.

See https://linuxconfig.org/how-to-install-cuda-on-ubuntu-20-04-focal-fossa-linux

See https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ for list of debs

    wget -O /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
    sudo add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"

    sudo apt install cuda libcudnn8 libcudnn8-dev

    # add to your path in .bashrc or whatever, you might already have /usr/local/cuda linked to this anyway
    export PATH=/usr/local/cuda-11.2/bin${PATH:+:${PATH}}
    export LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

    # rebash and check
    nvcc --version
    nvcc: NVIDIA (R) Cuda compiler driver
    Copyright (c) 2005-2021 NVIDIA Corporation
    Built on Thu_Jan_28_19:32:09_PST_2021
    Cuda compilation tools, release 11.2, V11.2.142
    Build cuda_11.2.r11.2/compiler.29558016_0


    # test with something
    tensorfow/check_gpu.py

    # still not yet working but this dodgy symlink, could also downgrade
    sudo ln -s /usr/local/cuda-11.2/targets/x86_64-linux/lib/libcusolver.so.11 /usr/local/cuda-11.2/targets/x86_64-linux/lib/libcusolver.so.10

    If you are trying the nvcc compile test from that site

    nvcc -o hello hello.cu

    You will need to install the right version of g++, probably sudo apt install g++-8 and then see.

