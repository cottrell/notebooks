https://hub.docker.com/_/vault/

docker pull vault

Using the Container
We chose Alpine as a lightweight base with a reasonably small surface area for security concerns, but with enough functionality for development and interactive debugging.

Vault always runs under dumb-init, which handles reaping zombie processes and forwards signals on to all processes running in the container. This binary is built by HashiCorp and signed with our GPG key, so you can verify the signed package used to build a given base image.

Running the Vault container with no arguments will give you a Vault server in development mode. The provided entry point script will also look for Vault subcommands and run vault with that subcommand. For example, you can execute docker run vault status and it will run the vault status command inside the container. The entry point also adds some special configuration options as detailed in the sections below when running the server subcommand. Any other command gets exec-ed inside the container under dumb-init.

The container exposes two optional VOLUMEs:

/vault/logs, to use for writing persistent audit logs. By default nothing is written here; the file audit backend must be enabled with a path under this directory.
/vault/file, to use for writing persistent storage data when using thefile data storage plugin. By default nothing is written here (a dev server uses an in-memory data store); the file data storage backend must be enabled in Vault's configuration before the container is started.
The container has a Vault configuration directory set up at /vault/config and the server will load any HCL or JSON configuration files placed here by binding a volume or by composing a new image and adding files. Alternatively, configuration can be added by passing the configuration JSON via environment variable VAULT_LOCAL_CONFIG. Please note that due to a bug in the current release of Vault (0.6.0), you should not use the name local.json for any configuration file in this directory.
