Remember this:

    curl -fsSL https://code-server.dev/install.sh | sh
    sudo systemctl enable code-server@$USER.service

    $ cat ~/.config/code-server/config.yaml
    bind-addr: 0.0.0.0:8080
    auth: password
    password: xxxxxx
    cert: false

    sudo systemctl restart code-server@$USER.service
