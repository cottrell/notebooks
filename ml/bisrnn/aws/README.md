# notes

For ad hoc stuff, for example if you want a notebook, just do ec2.

setup security rule. add custom access for ssh and for tcp port 8888. use your ip.

# make sure to log in as ubuntu
ssh -i "~/.cred/aws/2017kp.pem" ubuntu@f504caf2732051b22316ae44b6d2b69b7797711d37c15991

jupyter notebook --ip=0.0.0.0 --no-browser
