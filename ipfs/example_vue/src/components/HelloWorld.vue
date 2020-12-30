<template>
  <div class="hello">
    <button v-on:click="loadIPFS">CLICK</button>
  </div>
</template>

<script>

const IPFS = require('ipfs-core')

async function main() {
    // const ipfs = await IPFS.create()
    // const ipfs = await IPFS.create({rrrr: 'here'})
    const ipfs = await IPFS.create({repo: String(Math.random() + Date.now()) })
    // note the errors should go away with libp2p-websockets 0.15 release
    const { cid } = await ipfs.add('Hello world')
    console.info(cid)
    // QmXXY5ZxbtuYj6DnfApLiGstzPN7fvSyigrRee3hDWPCaf
    // process.exit()
}


export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  methods: {
    loadIPFS: function() {
        console.log('loadIPFS start')
        main()
        console.log('loadIPFS done')
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
