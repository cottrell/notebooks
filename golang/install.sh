#!/bin/bash
# 1. Fetch the latest version filename from the Go JSON API
LATEST_GO=$(curl -s 'https://go.dev/dl/?mode=json' |
            grep -oE 'go[0-9.]+\.linux-amd64\.tar\.gz' |
            head -1)

# 2. Perform the update only if a version was found
if [ -n "$LATEST_GO" ]; then
    echo "Updating to $LATEST_GO..."

    # Remove existing installation
    sudo rm -rf /usr/local/go

    # Download and extract directly to /usr/local
    curl -sL "https://go.dev/dl/$LATEST_GO" | sudo tar -C /usr/local -xzf -

    # Refresh the shell's command hash
    hash -r

    echo "Done! Go is now $(go version)"
else
    echo "Error: Could not detect the latest Go version."
fi
