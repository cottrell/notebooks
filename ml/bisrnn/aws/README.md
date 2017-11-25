setup security rule. add custom access for ssh and for tcp port 8888. use your ip.

ssh -i "~/.cred/aws/2017kp.pem" ubuntu@ec2-54-229-197-102.eu-west-1.compute.amazonaws.com

jupyter notebook --ip=0.0.0.0 --no-browser
