#!/bin/sh -e
# run this FROM the hugo dir!
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
case $1 in
    init)
        hugo new site .
        git init
        # git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
        # echo 'theme = "ananke"' >> config.toml
        git submodule add https://github.com/alanorth/hugo-theme-bootstrap4-blog.git themes/hugo-theme-bootstrap4-blog
        echo 'theme = "hugo-theme-bootstrap4-blog"' >> config.toml
        # look at head-custom.html
        # see .gitignore
        ;;
    post)
        # whatever
        post=$2
        [[ "$post" ]] || post=newpost
        cd $DIR/hugoblog
        filename=content/notes/$post.md
        [[ -e $filename ]] || hugo new notes/$post.md
        vi $filename
        ;;
    serve)
        hugo server --buildDrafts -w
        ;;
    *)
        echo dunno
        exit 1
        ;;
esac
