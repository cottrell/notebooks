#!/bin/bash -e
# https://gist.github.com/myusuf3/7f645819ded92bda6677
if [[ $# -ne 1 ]]; then
    echo usage $0 submodule
    exit 1
fi

submodule=$1

git rm -r "$submodule"
git add .gitmodules
# git rm -r --cached $submodule
rm -rf ".git/modules/$submodule"
git config -f ".git/config" --remove-section "submodule.$submodule" 2> /dev/null

# Commit the change
# git commit -m "Remove submodule $submodule"
echo commit change manually
