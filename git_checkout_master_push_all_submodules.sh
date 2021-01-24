# git submodule foreach --recursive 'git checkout master; git push origin master; :'
git submodule foreach --recursive 'git checkout master && git push origin master & :'
git push origin master
