all:
	cat Makefile


KEY = /tmp/nginx.key
CERT = /tmp/nginx.crt
SECRET = /tmp/secret.json

cert:
	microk8s kubectl delete secrets nginxsecret
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $(KEY) -out $(CERT) -subj "/CN=nginxsvc/O=nginxsvc"
	microk8s kubectl create secret tls nginxsecret --key /tmp/nginx.key --cert /tmp/nginx.crt
	microk8s kubectl get secrets

apply:
	microk8s kubectl apply -f nginx-secure-app.yaml
	microk8s kubectl create configmap nginxconfigmap --from-file=default.conf

delete:
	microk8s kubectl delete -f nginx-secure-app.yaml
	microk8s kubectl delete configmap nginxconfigmap
	microk8s kubectl get configmaps

get_ip:
	mk describe svc
	# then curl what shows up
	# microk8s kubectl get svc my-nginx -o yaml | grep nodePort -C 5
	# microk8s kubectl get nodes -o yaml | grep ExternalIP -C 1
