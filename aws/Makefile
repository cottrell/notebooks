all:
	cat Makefile


install:
	[ -e awscliv2.zip ] || curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
	unzip awscliv2.zip
	sudo ./aws/install
	echo remember to clean up

clean:
	dl aws awscliv2.zip
