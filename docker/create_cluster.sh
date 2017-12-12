#!/usr/bin/env bash

function create {
    echo "---Create $1"
    docker-machine create --swarm-image ubuntu:16.04 --driver virtualbox $1
}

create manager-1

manager_ip=$(docker-machine ip manager-1)

echo "---Swarm Init"
docker-machine ssh manager-1 docker swarm init --listen-addr ${manager_ip} --advertise-addr ${manager_ip}
docker-machine ssh manager-1 docker node update --label-add node.hostname=manager-1 manager-1

printf "\n---Get Tokens\n"
manager_token=$(docker-machine ssh manager-1 docker swarm join-token -q manager)
worker_token=$(docker-machine ssh manager-1 docker swarm join-token -q worker)

for n in {2..3} ; do
	name=manager-${n}
	printf "\n---Create ${name}\n"
	create ${name}
	ip=$(docker-machine ip ${name})
	echo "--- Swarm Manager Join"
	docker-machine ssh ${name} docker swarm join --listen-addr ${ip} --advertise-addr ${ip} --token ${manager_token} ${manager_ip}:2377
	docker-machine ssh ${name} docker node update --label-add node.hostname=${name} ${name}
done

for n in {1..3} ; do
	name=worker-${n}
	printf "\n---Create ${name}\n"
	create ${name}
	ip=$(docker-machine ip ${name})
	echo "--- Swarm Worker Join"
	docker-machine ssh ${name} docker swarm join --listen-addr ${ip} --advertise-addr ${ip} --token ${worker_token} ${manager_ip}:2377
	docker-machine ssh manager-1 docker node update --label-add node.hostname=${name} ${name}
done

printf "\n\n------------------------------------\n"
echo "To connect to your cluster..."
echo 'eval $(docker-machine env manager-1)'
