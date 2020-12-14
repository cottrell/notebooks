# DO NOT INSTALL VIA NPM!

# Can you have dats of dats?


    dat create --dir toplevel -y
    cd toplevel
    dat create --dir a -y
    dat create --dir b -y
    dat create --dir c -y

    dat clone 3640b779159e81950338b41d3c5486cb1ce1b66dd913fd4c3dc049cfab060b71 a_sync
    ls a/.dat
content.bitfield  content.key  content.signatures  content.tree  metadata.bitfield  metadata.data  metadata.key  metadata.ogd  metadata.signatures  metadata.tree
    ls a_sync/.dat/
content.bitfield  content.key  content.signatures  content.tree  metadata.bitfield  metadata.data  metadata.key  metadata.latest  metadata.signatures  metadata.tree


# Using dat

    mkdir -p datshare
    dat share ./datshare

    # get the hash
    dat clone dat://b3a94b7ea900e10ac0857d5ebe352fa9522b011829a6499d95a56466a74dc113 ./datshare2
    dat sync ./datshare2



    hyperdrive
