# notes

    sudo apt-get install git git-lfs make

## setup

To avoid github bandwidth limits, if possible use rsync from another machine.

    rsync -Wav --progress machine:~/projects projects

instead of

    git clone --recursive

but maybe git clone from machine also works.

    git submodule update --init ## if anything fails part way


## convenience

    make
    make pull
    make push


## TODO: vscode

https://github.com/microsoft/pyright/blob/main/docs/configuration.md

## Mark submodule as inactive

    git config -f .gitmodules submodule.superbasic.active false
    git status # see .gitmodules is updated
