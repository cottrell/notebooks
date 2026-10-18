# Fallback binary into this dir. Canonical install is apt + dashboard token
# (see Makefile). Do not use make login on the gmail Cloudflare account.
curl -L -o cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared
