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

NOTE: as of 2025-06-18 this does not really work.

    git config -f .gitmodules submodule.superbasic.active false
    git status # see .gitmodules is updated

    # perhaps test with this:
    git submodule foreach 'echo $name'

    git config --local --get-regexp submodule\..*\.active

NOTE: `.git/config` are local over-rides.

    git config -f .gitmodules --get-regexp '^submodule\..*\.active$' | while read key val; do  git config "$key" "$val"; done
    git config --local --get-regexp submodule\..*\.active
    cat .git/config
    git submodule update --init --recursive  # will this work? no.
