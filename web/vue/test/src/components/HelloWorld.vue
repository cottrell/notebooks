<template>
  <div class="hello">
    <div id="vis"></div>
    <h1>{{ msg }}</h1>
    <h2>{{ a }}</h2>
    <h2>{{ name }}</h2>
    <h2>{{ stuff }}</h2>
  </div>
</template>

<script>
import embed from 'vega-embed';
var spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
  "description": "asdfasdf",
  data: {
    values: [
    {'symbol': 'MSFT', 'date': 'Jan 1 2000', 'price': 39.81},
    {'symbol': 'MSFT', 'date': 'Feb 1 2000', 'price': 36.35},
    {'symbol': 'MSFT', 'date': 'Mar 1 2000', 'price': 43.22},
    {'symbol': 'MSFT', 'date': 'Apr 1 2000', 'price': 28.37},
    {'symbol': 'MSFT', 'date': 'May 1 2000', 'price': 25.45},
    {'symbol': 'MSFT', 'date': 'Jun 1 2000', 'price': 32.54},
    {'symbol': 'MSFT', 'date': 'Jul 1 2000', 'price': 28.4},
    {'symbol': 'MSFT', 'date': 'Aug 1 2000', 'price': 28.4},
    {'symbol': 'MSFT', 'date': 'Sep 1 2000', 'price': 24.53},
    {'symbol': 'MSFT', 'date': 'Oct 1 2000', 'price': 28.02},
    ]
  },
  // "data": {"url": "data/stocks.csv"},
  // "transform": [{"filter": "datum.symbol==='MSFT'"}],
  "mark": "line",
  "encoding": {
    "x": {"field": "date", "type": "temporal"},
    "y": {"field": "price", "type": "quantitative"}
  }
}

embed('#vis', spec);

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
    getData(){
      fetch('http://localhost:8000/data/yahoo?symbol=aapl', {mode:'cors'}).then(data => data.json()).then(data => {this.stuff = data;}).catch(err => console.log('Fetch Error :-S', err));
    }
  },
  mounted() {
    this.stuff = this.getData();
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
