vscode:

https://www.digitalocean.com/community/tutorials/how-to-set-up-the-code-server-cloud-ide-platform-on-ubuntu-18-04-quickstart

See previous [releases](https://code.visualstudio.com/updates/v1_52) here.

    sudo snap install --classic code
    sudo snap install --classic code --channel=latest/beta
    snap info code # list versions


Remember this:

    curl -fsSL https://code-server.dev/install.sh | sh
    sudo systemctl enable code-server@$USER.service

    $ cat ~/.config/code-server/config.yaml
    bind-addr: 0.0.0.0:8080
    auth: password
    password: xxxxxx
    cert: false

    sudo systemctl restart code-server@$USER.service

Remember the vscode-pdf plugin to make pdfs work.
