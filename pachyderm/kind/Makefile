# NOTE: make sure you get rid of old pachctl version or at least are using the new correct one after installing

all:
	cat Makefile

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

install_kind:
	curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.14.0/kind-linux-amd64
	chmod +x ./kind
	sudo mv ./kind /usr/local/bin/kind
	kind version

install_helm:
	curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
	chmod 700 get_helm.sh
	./get_helm.sh
	helm version

install_pachctl:
	curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v2.2.7/pachctl_2.2.7_amd64.deb && sudo dpkg -i /tmp/pachctl.deb
	pachctl version --client-only

create_cluster:
	kind create cluster
	kubectl cluster-info --context kind-kind
	kubectl cluster-info dump


deploy_pachyderm:
	# https://docs.pachyderm.com/latest/getting-started/local-installation/#deploy-pachyderm
	helm repo add pach https://helm.pachyderm.com
	helm repo update
	# do this in a separate tab while waiting: helm list --all
	helm install --wait --timeout 10m pachd pach/pachyderm --set deployTarget=LOCAL
	# check
	kubectl get pods

check_install:
	kubectl get pods
	# should see 5 entries something like:
	# NAME                                           READY   STATUS      RESTARTS   AGE
	# pod/console-5b67678df6-s4d8c                   1/1     Running     0          2m8s
	# pod/etcd-0                                     1/1     Running     0          2m8s
	# pod/pachd-c5848b5c7-zwb8p                      1/1     Running     0          2m8s
	# pod/pg-bouncer-7b855cb797-jqqpx                1/1     Running     0          2m8s
	# pod/postgres-0                                 1/1     Running     0          2m8s

connect_pachyderm:
	pachctl config import-kube local --overwrite
	pachctl config set active-context local
	pachctl port-forward # this blocks, background this process in a new tab of your terminal
	# to connect do something like
	# ssh -v -N -f -L localhost:4000:localhost:4000 remote_host

verify_pachyderm:
	pachctl version
	# COMPONENT           VERSION
	# pachctl             2.2.7
	# pachd               2.2.7

# uninstall:
# helm uninstall pachd
# kubectl delete pvc -l suite=pachyderm

listing_things:
	pachctl list repo
	pachctl list file images_delightful-peccary@master
	# delete demo
	# pachctl delete pipeline montage_delightful-peccary && pachctl delete pipeline edges_delightful-peccary && pachctl delete repo images_delightful-peccary


pause:
	docker ps -a
	docker pause kind-control-plane
	docker ps -a

unpause:
	docker ps -a
	docker unpause kind-control-plane
	docker ps -a
