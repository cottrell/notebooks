all:
	cat Makefile

install:
	curl -sfL https://get.k3s.io | sh -

start:
	sudo k3s server &

stop:
	k3s-killall.sh

check:
	# Check for Ready node,
	#   takes maybe 30 seconds
	k3s kubectl get node
