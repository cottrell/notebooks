#!/bin/sh -e
# rhel7 cluster as script instead of README.md
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# swarm_image=registry.access.redhat.com/rhel7/rhel
swarm_image=centos
n_nodes=3
function vms() {
    for x in $(seq 0 $(($n_nodes - 1))); do echo vm$x; done
}
manager=$(vms | head -1)
others=$(vms | tail -n +2)

case $1 in
    pull)
	docker pull $swarm_image
        ;;
    create)
        for x in $(vms); do
	    # docker-machine create --swarm-image $swarm_image --driver virtualbox $x
	    docker-machine create --swarm-image $swarm_image $x
        done
        ;;
    setup)
	docker-machine ssh $manager "docker swarm init --advertise-addr 192.168.99.100" || echo HELLO HUMAN: manager is probably already setup. Will just retrieve token.
        token=$(docker-machine ssh $manager "docker swarm join-token worker -q")
        for x in $others; do
	    docker-machine ssh $x "docker swarm join --token $token 192.168.99.100:2377" || echo HELLO HUMAN: working is already part of swarm. Skipping.
        done
        ;;
    ls)
        docker-machine ls $(vms)
        ;;
    ls_nodes)
        docker-machine ssh $manager "docker node ls"
        ;;
    env)
        docker-machine env $manager
        ;;
    start)
        docker-machine start $(vms)
        ;;
    stop)
        docker-machine stop $(vms)
        ;;
    i)
        # interactive, sudo -i for root
        docker-machine ssh $manager -i /bin/bash
        ;;
    delete_all)
        echo docker-machine rm $(vms)
        docker-machine rm $(vms) # Delete all VMs and their disk images
        ;;
    *)
        echo unknown command
        exit 1
        ;;
esac

