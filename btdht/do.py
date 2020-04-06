import btdht
import binascii
dht = btdht.DHT()
def start():
    dht.start()
    print('now wait at least 15s for the dht to boostrap')

def get_peers(hash_):
    # copy paste the hash printed by start
    dht.get_peers(binascii.a2b_hex(hash_))
    # seems to always return no peers
