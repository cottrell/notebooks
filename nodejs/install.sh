#!/bin/bash
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
# in lieu of restarting the shell
source "$HOME/.nvm/nvm.sh"
# Download and install Node.js:
nvm install node
nvm install 22
nvm install 20
# nvm alias default 20  # Set 20 as default for Claude compatibility
# Verify:
node -v # Should print "v20.x.x" (not v22)
nvm current # Should print "v20.x.x"
npm -v
