from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

bdb = BigchainDB('https://test.bigchaindb.com')
alice = generate_keypair()
tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset={'data': {'message': 'Blockchain all the things!'}})
signed_tx = bdb.transactions.fulfill(
    tx,
    private_keys=alice.private_key)
bdb.transactions.send_commit(signed_tx)
