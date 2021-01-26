all:
	cat Makefile

install:
	sudo snap install microk8s --classic

start:
	sudo microk8s start

stop:
	sudo microk8s stop

status:
	microk8s status --wait-ready

enable:
	microk8s enable dashboard # dns registry istio

cert:
	openssl req -nodes -newkey rsa:2048 -keyout dashboard.key -out dashboard.csr -subj "/C=/ST=/L=/O=/OU=/CN=*"
	openssl x509 -req -sha256 -days 3650 -in dashboard.csr -signkey dashboard.key -out dashboard.crt

	microk8s kubectl -n kube-system delete secret kubernetes-dashboard-certs
	microk8s kubectl -n kube-system create secret generic kubernetes-dashboard-certs --from-file=dashboard.crt --from-file=dashboard.key
	microk8s kubectl -n kube-system edit deploy kubernetes-dashboard -o yaml

	# then edit the yaml to look like this:
	#           args:
	#             - --tls-cert-file=dashboard.crt
	#             - --tls-key-file=dashboard.key
	#             #- --auto-generate-certificates

dashboard:
	microk8s dashboard-proxy

ns:
	microk8s kubectl get all --all-namespaces

dash:
	# this should be avail on the LAN
	sudo microk8s dashboard-proxy --address 0.0.0.0 --tls-cert-file=dashboard.crt --tls-key-file=dashboard.key

