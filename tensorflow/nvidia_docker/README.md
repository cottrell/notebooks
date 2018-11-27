https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce

sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# verify
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
# make sure you get stable version
sudo apt-get install docker-ce
# there are details to install specific versions on the page

# test
sudo docker run hello-world
