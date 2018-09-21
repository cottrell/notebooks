---
title: "Setting up Hugo"
date: 2018-09-20T20:14:41+01:00
draft: false
---

{{< highlight sh >}}
mkdir newsite && cd newsite
hugo new site .
git init # assume you are in git repo already
git submodule add https://github.com/alanorth/hugo-theme-bootstrap4-blog.git themes/
echo 'theme = "hugo-theme-bootstrap4-blog"' >> config.toml
git commit

cat >layouts/partials/head-custom.html<<EOL
<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.js"></script>
EOL

cat >.gitignore<<EOL
# Hugo default output directory
/public

## OS Files
# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# OSX
.DS_Store
EOL
{{< / highlight >}}
