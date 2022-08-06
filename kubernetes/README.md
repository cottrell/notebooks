# 2022

https://earthly.dev/blog/k8s-dev-solutions/

Seems like:
* microk8s is full product (is from Canonical).
* k3s lightweight, not a development tool, meant to be installed as lightweight on iot etc.
* minikube, used to be most popular. Not a full fledged thing? And I remember hating it.


So next time try k3s, microk8s and for pachyderm will use kind.


But for pachyderm local deployment, they seem to only include
* docker desktop
* minikube
* kind
* oracle virtualbox

Consider just using kind to begin with.

https://blog.frankel.ch/goodbye-minikube/

# 2021

Maybe just https://www.kubeflow.org/docs/started/getting-started/ ?

Trying to understand best devflow for dockerless approach.

Seems microk8s is central choice for k8s.  `sudo snap install microk8s --classic`

Seems skaffold is a reasonable build system to start with.

What about secrets?

What is skaffold? https://towardsdatascience.com/kubernetes-local-development-the-correct-way-1bc4b11570d8

What is Draft? https://codefresh.io/howtos/local-k8s-draft-skaffold-garden/

What is Garden?

What is Helm?

What is Jib? Some dockerfile build thing but seems java oriented.

What is Kustomize?

What is podman? https://podman.io/getting-started/

What is kaniko? https://github.com/GoogleContainerTools/kaniko
