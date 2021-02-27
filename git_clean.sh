echo before: $(du -sh)
git submodule foreach --recursive 'git reflog expire --all --expire=now && git gc --prune=now --aggressive & :'
echo after: $(du -sh)
