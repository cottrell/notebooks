git pull # you forget this
git submodule foreach --recursive 'git checkout master; git pull origin master:master; :'
