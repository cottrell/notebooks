# 2021-02

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

The steps are precisely:

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


## Tensorflow

https://www.tensorflow.org/install/gpu

I think that the location might have changed on 20.04.  Old one is this

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64








https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-20-04-focal-fossa-linux


Detect:
    ubuntu-drivers devices
    == /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
    modalias : pci:v000010DEd00001F02sv000019DAsd00002516bc03sc00i00
    vendor   : NVIDIA Corporation
    model    : TU106 [GeForce RTX 2070]
    driver   : nvidia-driver-418-server - distro non-free
    driver   : nvidia-driver-450-server - distro non-free
    driver   : nvidia-driver-450 - distro non-free
    driver   : nvidia-driver-460 - third-party non-free recommended
    driver   : xserver-xorg-video-nouveau - distro free builtin

    ubuntu-drivers devices
    sudo add-apt-repository ppa:graphics-drivers/ppa
    == /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
    modalias : pci:v000010DEd00001F02sv000019DAsd00002516bc03sc00i00
    vendor   : NVIDIA Corporation
    model    : TU106 [GeForce RTX 2070]
    driver   : nvidia-driver-460 - third-party non-free recommended
    driver   : nvidia-driver-418-server - distro non-free
    driver   : nvidia-driver-450-server - distro non-free
    driver   : nvidia-driver-450 - distro non-free
    driver   : xserver-xorg-video-nouveau - distro free builtin

Have tried:
    sudo apt install nvidia-driver-460
    sudo apt install nvidia-driver-455
    sudo apt install nvidia-driver-450
    sudo ubuntu-drivers autoinstall


## Ongoing from tensorflow docs
## Add NVIDIA package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update

wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb

sudo apt install ./nvidia-machine-learning-repo-ubuntu2004_1.0.0-1_amd64.deb
sudo apt-get update

## Install NVIDIA driver
THIS PART FAILS CAN NOT INSTALL
E: Unable to correct problems, you have held broken packages.
sudo apt-get install --no-install-recommends nvidia-driver-450
## Reboot. Check that GPUs are visible using the command: nvidia-smi

wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/libnvinfer7_7.1.3-1+cuda11.0_amd64.deb
sudo apt install ./libnvinfer7_7.1.3-1+cuda11.0_amd64.deb
sudo apt-get update

## Install development and runtime libraries (~4GB)
sudo apt-get install --no-install-recommends \
    cuda-11-0 \
    libcudnn8=8.0.4.30-1+cuda11.0  \
    libcudnn8-dev=8.0.4.30-1+cuda11.0


## Install TensorRT. Requires that libcudnn8 is installed above.
sudo apt-get install -y --no-install-recommends libnvinfer7=7.1.3-1+cuda11.0 \
    libnvinfer-dev=7.1.3-1+cuda11.0 \
    libnvinfer-plugin7=7.1.3-1+cuda11.0





Test:
    nvidia-smi




Not working:

    # REBOOT
    nvidia-detector # outputs nvidia-driver-460
    sudo apt install nvidia-driver-460
    # REBOOT
    nvidia-smi
    fails
    sudo apt install nvidia-driver-455
    ...

https://www.cyberciti.biz/faq/ubuntu-linux-install-nvidia-driver-latest-proprietary-driver/
https://askubuntu.com/questions/1307160/nvidia-drivers-reset-after-update-and-now-monitor-is-unknown-and-stuck-in-640x
