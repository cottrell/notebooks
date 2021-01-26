all:
	cat Makefile
start:
	sudo microk8s start

stop:
	sudo microk8s stop

status:
	microk8s status --wait-ready

enable:
	microk8s enable dashboard dns registry istio

ns:
	microk8s kubectl get all --all-namespaces

dash:
	echo you will probably need to ssh tunnel if you are on another computer
	echo tunnel.sh bleepblop 10443
	sudo microk8s dashboard-proxy --address 0.0.0.0 --tls-cert-file=dashboard.crt --tls-key-file=dashboard.key

cert:
	mkdir -p certs
	openssl req -nodes -newkey rsa:2048 -keyout certs/dashboard.key -out certs/dashboard.csr -subj "/C=/ST=/L=/O=/OU=/CN=*"
	openssl x509 -req -sha256 -days 3650 -in certs/dashboard.csr -signkey certs/dashboard.key -out certs/dashboard.crt
	kubectl -n kube-system delete secret kubernetes-dashboard-certs
	kubectl -n kube-system create secret generic kubernetes-dashboard-certs --from-file=dashboard.crt --from-file=dashboard.key
	kubectl -n kube-system edit deploy kubernetes-dashboard -o yaml
