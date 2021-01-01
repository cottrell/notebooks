# IPFS Notes

tldr; say simple and just use `ipfs add -Q filename`.

tldr; remember you need to run `ipfs daemon` on both machines it seems (if you are using the cli at least, not sure about the js core lib).

Remember ipns of dnslink (faster but requires a domain you own ... uses dns) for naming and updates.

See the Makefile.

Remember `ipfs files` to interact with objects as if they were a unix filesytem. Probably not that useful to begin with.

# Misc

https://github.com/ipfs/py-ipfs-http-client

See this https://github.com/ipld/py-cid

    ipfs refs local
    ipfs cat /ipfs/QmS4ustL54uo8FzR9455qaxZwuMiUhyvMcX9Ba8nUH4uVv/readme
    ipfs pin add hash

Still not sure how to add key value pair. There is some dht command but seems like folks are pointing toward ifps name.

    ipfs key gen what -t rsa
    ipfs name publish -k what QmNvHfPKyGF7vPGAhs255kJ96N6ZbWAbgtHuT8pdv63sa6

More

    echo yes > no.txt
    ipfs add no.txt
    added QmdXUxyfi5KDncqspLxBmdKFVijQhbRN5gMVrywi3zgZqw no
    4 B / 4 B [==============================] 100.00%


