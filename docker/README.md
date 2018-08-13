# .

	cd <somewhere>
	docker build . -t name_here

	docker run -it name_here /bin/bash

	docker run -it centos:latest /bin/bash

	docker network inspect bridge

	docker network inspect bridge --format='{{json .IPAM.Config}}'

	docker run --network host
	docker run --network host -it centos_postgres /bin/bash
