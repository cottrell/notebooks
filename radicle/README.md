# setup

https://radicle.xyz/

curl -sSf https://radicle.xyz/install | sh

see ~/.radicle ... you can delete it to start from scratch and `rad auth` to set up.

## flow

A
```
mkdir rad_example
cd rad_example
git init .
echo "look" > README.md
git add README.md
git commit -m "first"
rad init .
rad .  # get repo id
```

B
```
rad clone <repo_id>
cd rad_example
# <edit> README
git add README.md
git commit -m 'third'
ssh-add ~/.radicle/keys/radicle
git push
git push rad  # not sure
rad sync
```

A
```
rad remote add <nid>
rad sync
git branch -a # find branch for now
git log <branch> # see commit
git merge <branch>
git push rad # update rad/main
rad sync
```
