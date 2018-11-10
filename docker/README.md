# .

https://medium.com/travis-on-docker/how-to-version-your-docker-images-1d5c577ebf54

https://markshust.com/2018/01/30/performance-tuning-docker-mac

    # USE docker run -v delegated

	cd <somewhere>
	docker build . -t name_here

	docker run -it name_here /bin/bash

	docker run -it centos:latest /bin/bash

	docker network inspect bridge

	docker network inspect bridge --format='{{json .IPAM.Config}}'

	docker run --network host
	docker run --network host -it centos_postgres /bin/bash
