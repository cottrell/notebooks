# 2025-05-06

See Makefile

# 2025-03-10


To avoid using sudo for everything.

    mkdir -p ~/.npm-global
    npm config set prefix '~/.npm-global'
    echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
