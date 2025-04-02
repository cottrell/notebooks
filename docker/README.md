# 2025-03-20

Debug (why so many running in htop?)

```
sudo apt remove --purge docker.io
sudo apt install docker.io
```


# 2023-12-20

Official instructions on docker site no longer work.

    apt install docker.io

Then do the docker group thing here https://docs.docker.com/engine/install/linux-postinstall/

# 2023-10-20

	docker stop test_container
	docker rm test_container
	docker build . -t test
	docker run -d --name test_container test
	docker exec -it test_container /bin/bash

Never install via snap. Use official docker page.

# 2023-01-30

Reminders.

    Docker build .  # fails
    docker run -it --rm id /bin/bash  # debug
    etc


    docker exec for running containers

# Ports

NETWORK HOST NETWORK HOST NETWORK HOST!!!! IS IMPORTANT.

https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach

Edit: If you are using Docker-for-mac or Docker-for-Windows 18.03+, just connect to your mysql service using the host host.docker.internal.

As of Docker 18.04, this does not work on Docker-for-Linux. However, using a container as described in qoomon's answer you can get it to work.

TLDR
Use --network="host" in your docker run command, then 127.0.0.1 in your docker container will point to your docker host.

Note: This mode only works on Docker for Linux, per the documentation.


# Build

You always forget.

    docker build -t username/image_name:tag_name .

Debug failed build:


     docker run -it --rm 9414288adf15 /bin/bash

# Commands


    docker run --network="host" ... --name blah image_name cmd

    docker exec -it name_here /bin/bash


https://medium.com/travis-on-docker/how-to-version-your-docker-images-1d5c577ebf54

https://markshust.com/2018/01/30/performance-tuning-docker-mac

    # USE docker run -v delegated

	cd <somewhere>
	docker build . -t name_here

	docker network inspect bridge

	docker network inspect bridge --format='{{json .IPAM.Config}}'

	docker run --network host
	docker run --network host -it centos_postgres /bin/bash
