#!/bin/bash -e

echo run this line by line
echo run this line by line
echo run this line by line
echo run this line by line
echo run this line by line
echo run this line by line

sleep 5

# Generate and trust a self-signed cert for local HTTPS development

# Step 1: Get LAN IP
IP=$(ip route get 1 | awk '{print $7; exit}')
echo "Detected LAN IP: $IP"

# Step 2: Generate OpenSSL config with SAN
cat > san.cnf <<EOF
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = $IP

[v3_req]
subjectAltName = @alt_names

[alt_names]
IP.1 = $IP
EOF

# Step 3: Generate cert and key
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes -config san.cnf -extensions v3_req

# Step 4: Strip private key for system store
openssl x509 -in cert.pem -out clean.crt

echo you might need to delete some not sure
# # Step 4b: Clean up system trust store
# echo "Removing old system cert if present..."
# sudo rm -f /usr/local/share/ca-certificates/$IP.crt
# sudo rm -f /etc/ssl/certs/$IP.pem || true
# sudo update-ca-certificates --fresh

# Step 5: Install into system trust store
sudo rm -f /usr/local/share/ca-certificates/$IP.crt
sudo cp clean.crt /usr/local/share/ca-certificates/$IP.crt
sudo update-ca-certificates

# Step 6: Install into Chrome NSS DB
echo "Installing into Chrome's NSS DB..."
CERT_NICK="Local Dev Cert"
mkdir -p "$HOME/.pki/nssdb"
certutil -d sql:$HOME/.pki/nssdb -D -n "$CERT_NICK" 2>/dev/null || true
certutil -A -d sql:$HOME/.pki/nssdb -n "$CERT_NICK" -t "C,," -i cert.pem

echo "✅ All done. Restart Chrome and access: https://$IP:8443/"

