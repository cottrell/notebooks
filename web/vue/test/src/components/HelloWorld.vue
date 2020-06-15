<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <my-chart v-bind:spec="first_spec"></my-chart>
  </div>
</template>

<script>
import MyChart from './MyChart.vue';

var spec_a = {
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
  // "transform": [{"filter": "datum.symbol==='MSFT'"}],
  "mark": "line",
  "encoding": {
    "x": {"field": "date", "type": "temporal"},
    "y": {"field": "price", "type": "quantitative"}
  }
}

export default {
  name: 'HelloWorld',
  components: {
    MyChart
  },
  props: {
    msg: String,
  },
  data: function() {
    return {
            first_spec: spec_a,
            };
        },
  methods: {
    getData(){
      fetch('http://localhost:8000/data/yahoo?symbol=aapl', {mode:'cors'}).then(data => data.json()).then(data => {this.stuff = data;}).catch(err => console.log('Fetch Error :-S', err));
    }
  },
  mounted() {
    // this.stuff = this.getData();
  },
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
