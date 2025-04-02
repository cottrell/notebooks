# I used to install via conda-forge see /python

sudo apt install nodejs npm


# 2025-03-10


To avoid using sudo for everything.

    mkdir -p ~/.npm-global
    npm config set prefix '~/.npm-global'
    echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
