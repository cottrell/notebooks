#!/bin/bash -ex
mkdir newhugosite
cd newhugosite
hugo new site .
git init
# git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
# echo 'theme = "ananke"' >> config.toml
git submodule add https://github.com/alanorth/hugo-theme-bootstrap4-blog.git themes/hugo-theme-bootstrap4-blog
echo 'theme = "hugo-theme-bootstrap4-blog"' >> config.toml
echo look at head-custom.html
echo see .gitignore

