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
	microk8s enable dashboard # dns
	microk8s enable dns # you need this probably all the time
	# microk8s enable registry # this is for docker, I am trying the manual tar include:
	# 	docker save our/docs:local > our_docs_local.tar
	# 	microk8s ctr image import our_docs_local.tar
	# microk8s enable istio # dunno if needed generally
	microk8s enable metallb  # need this for ExternalIP https://stackoverflow.com/questions/65985098/no-externalip-showing-in-kubernetes-nodes/65991935#65991935
	microk8s enable ingress  # not sure if needed for above

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

ns:
	microk8s kubectl get all --all-namespaces

dash:
	# this should be avail on the LAN
	sudo microk8s dashboard-proxy --address 0.0.0.0 --tls-cert-file=dashboard.crt --tls-key-file=dashboard.key

example_yaml:
	microk8s kubectl run nginx --image=nginx --dry-run -o yaml

help_yaml:
	microk8s kubectl explain pod.spec
