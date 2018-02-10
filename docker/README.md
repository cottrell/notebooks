# Get Docker for Mac (Stable)

do not use brew

	wget https://download.docker.com/mac/stable/Docker.dmg

	https://zaiste.net/posts/removing_docker_containers/

	docker ps -aq --no-trunc | xargs docker rm

https://hub.docker.com/_/ubuntu/

	docker pull ubuntu

	docker run -i -t ubuntu:16.04 /bin/bash

To see docker file from image:

	docker history --no-trunc <img>

# cluster

	See `do.sh`

	docker-machine create --swarm-image ubuntu:16.04 --driver virtualbox vm0
	docker-machine create --swarm-image ubuntu:16.04 --driver virtualbox vm1

	docker-machine ls

	docker-machine ssh vm0 "docker swarm init --advertise-addr 192.168.99.100"
	docker-machine ssh vm1 "docker swarm join --token <token> 192.168.99.100:2377"

	docker-machine ssh vm1 "docker node ls"
	docker-machine env vm0

	docker-machine create --driver virtualbox myvm1 # Create a VM (Mac, Win7, Linux)

	https://docs.docker.com/get-started/part4

	docker-machine create -d hyperv --hyperv-virtual-switch "myswitch" myvm1 # Win10
	docker-machine env myvm1                # View basic information about your node
	docker-machine ssh myvm1 "docker node ls"         # List the nodes in your swarm
	docker-machine ssh myvm1 "docker node inspect <node ID>"        # Inspect a node
	docker-machine ssh myvm1 "docker swarm join-token -q worker"   # View join token
	docker-machine ssh myvm1   # Open an SSH session with the VM; type "exit" to end
	docker node ls                # View nodes in swarm (while logged on to manager)
	docker-machine ssh myvm2 "docker swarm leave"  # Make the worker leave the swarm
	docker-machine ssh myvm1 "docker swarm leave -f" # Make master leave, kill swarm
	docker-machine ls # list VMs, asterisk shows which VM this shell is talking to
	docker-machine start myvm1            # Start a VM that is currently not running
	docker-machine env myvm1      # show environment variables and command for myvm1
	docker stack deploy -c <file> <app>  # Deploy an app; command shell must be set to talk to manager (myvm1), uses local Compose file
	docker-machine scp docker-compose.yml myvm1:~ # Copy file to node's home dir (only required if you use ssh to connect to manager and deploy the app)
	docker-machine ssh myvm1 "docker stack deploy -c <file> <app>"   # Deploy an app using ssh (you must have first copied the Compose file to myvm1)
	eval $(docker-machine env -u)     # Disconnect shell from VMs, use native docker
	docker-machine stop $(docker-machine ls -q)               # Stop all running VMs
	docker-machine rm $(docker-machine ls -q) # Delete all VMs and their disk images
