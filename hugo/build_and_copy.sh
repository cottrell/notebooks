#!/bin/sh -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/hugoblog
dl public/
# TODO need to exclude drafts
./build_search_index_and_commit.sh || :
hugo --baseURL https://cottrell.github.io/notebooks/
mkdir -p ../../docs
cp -vR public/* ../../docs

# fragile stuff
rm ../../docs/js/lunr/PagesIndex_dev.json
# mv ../../docs/js/lunr/PagesIndex{_prod,}.json

cmd="cd $DIR/.. && ls && git add ./docs && git commit -m 'update docs' && git push"
echo
read -p "RUN command $cmd ? " -n 1 -r </dev/tty
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo got yes
    eval $cmd
else
    echo
    echo not committing and pushing
fi
