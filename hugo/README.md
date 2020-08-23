# Quickstart

    mkdir newhugosite
    cd newhugosite
    git init
    hugo new site .
    git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
    echo 'theme = "ananke"' >> config.toml
    git submodule add https://github.com/alanorth/hugo-theme-bootstrap4-blog.git themes/
    echo 'theme = "hugo-theme-bootstrap4-blog"' >> config.toml
    echo look at head-custom.html
    echo see .gitignore

