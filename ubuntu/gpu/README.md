# 2021

On Ubuntu 20.04.

Run purge between any attempts:
    ./nvidia_purge.sh
    ./cuda_purge.sh

https://www.tensorflow.org/install/gpu

This guy blacklists nouveau: https://medium.com/@sargupta/fix-nvidia-smi-not-working-3c040ac426b3#:~:text=NVIDIA%2DSMI%20has%20failed%20because,driver%20is%20installed%20and%20running.&text=Then%20re%2Dadd%20the%20PPA%20and%20install%20the%20driver. But I tried that and it doesn't work.

There is this one but nothing there is new and it doesn't work https://linoxide.com/linux-how-to/how-to-install-nvidia-driver-on-ubuntu/
They do mention the desktop thing and nouveau: sudo apt install ubuntu-desktop

See issue on askubuntu.


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

## Install nvidia drivers

    sudo ubuntu-drivers autoinstall

    sudo reboot

I think that the location might have changed on 20.04.
Old one is this
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
