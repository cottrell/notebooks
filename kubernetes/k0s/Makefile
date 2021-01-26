all:
	cat Makefile

install_lens:
	sudo snap install kontena-lens --classic

install:
	curl -sSLf https://get.k0s.sh | sudo sh

install_kubectl:
	sudo curl --output /usr/local/sbin/kubectl -L "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"

init:
	mkdir -p ${HOME}/.k0s
	k0s default-config | tee ${HOME}/.k0s/k0s.yaml

start:
	sudo k0s server -c ${HOME}/.k0s/k0s.yaml --enable-worker &

create_node:
	#Create and add a worker node
	k0s token create --role=worker
	k0s worker MY_TOKEN
