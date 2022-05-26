all:
	cat Makefile

docker_cpu:
	# http://localhost:6273
	docker run -d -v $HOME/heavyai-docker-storage:/heavyai-storage -p 6273-6280:6273-6280 heavyai/heavyai-ee-cpu

docker_gpu:
	sudo docker run --runtime=nvidia \
		  	-d --runtime=nvidia \
		    	-v /var/lib/heavyai:/heavyai-storage \
		      	-p 6273-6280:6273-6280 \
		        heavyai/heavyai-ee-cuda:v5.5.5
