# As of 2019-03

Later version of nvidia drivers seem to be ok across the board for tf-nightly-gpu and tf 2.0.

Do a clean install/purge of nvidia and cuda (see ../ubuntu notes one level up).

Download latest nvidia cuda driver manually and follow the instructions there that usually look something like this:

    sudo dpkg -i ./cuda-repo-ubuntu1810-10-1-local-10.1.105-418.39_1.0-1_amd64.deb
    sudo apt-key add /var/cuda-repo-10-1-local-10.1.105-418.39/7fa2af80.pub
    sudo apt-get update
    sudo apt-get install cuda

Then there is some issue with 10-1 needing cusparse from 10-0, seems we need to download that manually and install as well:

    sudo dpkg -i ./cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb
    sudo apt-key add /var/cuda-repo-10-0-local-10.0.130-410.48/7fa2af80.pub
    sudo apt-get update
    sudo apt-get install cuda-10-0
