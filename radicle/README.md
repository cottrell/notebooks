https://radicle.xyz/

curl -sSf https://radicle.xyz/install | sh

see ~/.radicle ... you can delete it to start from scratch and `rad auth` to set up


Roughly (not quite)

    # 1st machine
    mkdir a
    cd a
    git init
    echo whatever > README.md
    git add README.md
    git commit -m 'Whatever'
    rad init
    git push
    rad node start

    ...

    # 2nd machine
    rad clone id
    ... commit something
    rad node start
    git push

    ...
    # now you need to add remote to 1st machin
    rad remote add nid
