Probably just best to use mkcert (see notebook dir).

Set up self cert for https on lan/dev etc.

See https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate/47646463

    create_root_cert_and_key.sh

    ./create_cert_for_domain.sh bleepblop
    Generating a RSA private key
    .....................................+++++
    .....................................................+++++
    writing new private key to 'device.key'
    -----
    Signature ok
    subject=C = CA, ST = None, L = NB, O = None, CN = *.bleepblop
    Getting CA Private Key

    ###########################################################################
    Done!
    ###########################################################################
    To use these files on your server, simply copy both bleepblop.csr and
    device.key to your webserver, and use like so (if Apache, for example)

        SSLCertificateFile    /path_to_your_files/bleepblop.crt
        SSLCertificateKeyFile /path_to_your_files/device.key


The run the copy script, then on the host do

    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain rootCA.pem

Test with something like

    http-server -S -C localhost+3.pem -K localhost+3-key.pem
