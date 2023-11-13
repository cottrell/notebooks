all:
	cat Makefile

# install_docker:
# 	docker pull ghcr.io/openbb-finance/openbbterminal-poetry:latest
# 	ifconfig | grep inet | grep -v -e "127.0.0.1" | awk '$1=="inet" { print $2 }'
# 	ifconfig | grep inet | grep -v -e "127.0.0.1" | awk '$1=="inet" { print $2 }'
# 	echo put in setenv:
# 	echo DISPLAY=IP:0
# 	echo GT_API_IEX_KEY=asdfasdf
#
# run_docker:
# 	docker run --env-file=./setenv -it --rm ghcr.io/openbb-finance/openbbterminal-poetry:latest

install:
	./install.sh
run:
	./run.sh
