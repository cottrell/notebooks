Never properly working on old macbook. Not sure if system root store is busted there. Try again on another os later.

See this example: https://matthewhoelter.com/2019/10/21/how-to-setup-https-on-your-local-development-environment-localhost-in-minutes.html
Also: https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/

You should see something like this in then end:

    mkcert -install
    The local CA is already installed in the system trust store! 👍
    The local CA is now installed in the Firefox and/or Chrome/Chromium trust store (requires browser restart)! 🦊

On hosts you probably need to faff with /etc/hosts to map the name and do something like this:

    sudo killall -HUP mDNSResponder

See this about becoming your own CA:

    https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate/47646463
