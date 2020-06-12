<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h2>{{ a }}</h2>
    <h2>{{ name }}</h2>
    <h2>{{ stuff }}</h2>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String,
  },
  data: function() {
    return {
            a: 2,
            stuff: '',
            name: ''
            };
        },
  methods: {
    getName(){
      fetch('http://localhost:8000/data/yahoo?symbol=aapl', {mode:'cors'}).then(data => data.json()).then(data => {this.stuff = data; console.log(data);}).catch(err => console.log('Fetch Error :-S', err));
    }
  },
  mounted() {
    this.stuff = this.getName();
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
