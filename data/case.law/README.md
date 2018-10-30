    xidel --extract "//a/@href" http://example.com/ https://case.law/bulk/download/ > hrefs.txt
    cat hrefs.txt | grep http | grep download > todo
    for x in $(cat todo); do
      wget $x -O tmp.zip
      unzip tmp.zip
      rm tmp.zip
    done
    rm todo
    rm hrefs.txt
