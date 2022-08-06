all:
	cat Makefile

install:
	curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.14.0/kind-linux-amd64
	chmod +x ./kind
	sudo mv ./kind /usr/local/bin/kind
	kind version


install_kubectl:
	# via curl:
	# curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
	# curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
	# echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
	# sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
	# kubectl version --client
	#
	# via apt-get:
	sudo apt-get update
	sudo apt-get install -y ca-certificates curl
	sudo apt-get install -y apt-transport-https
	# I think you do not need to run this multiple times for example:
	# sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
	# echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
	sudo apt-get update
	sudo apt-get install -y kubectl
	kubectl version --short

