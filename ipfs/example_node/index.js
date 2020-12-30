const IPFS = require('ipfs-core')

async function main() {
    const ipfs = await IPFS.create()
    const { cid } = await ipfs.add('Hello world')
    console.info(cid)
    // QmXXY5ZxbtuYj6DnfApLiGstzPN7fvSyigrRee3hDWPCaf
}

main()
