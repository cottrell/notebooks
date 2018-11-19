#!/usr/bin/env python
import json
import os
from cryptography.fernet import Fernet
import sys
message = sys.stdin.read().encode()

key = json.load(open(os.path.join(os.path.expanduser('~/.cred/weak/cred.json'))))['key'].encode()
f = Fernet(key)
decrypted = f.decrypt(message)
sys.stdout.write(decrypted.decode())
