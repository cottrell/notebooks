# ...

cd ~/dev
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

pip install redis

~/dev/redis-4.0.6/src/redis-server

