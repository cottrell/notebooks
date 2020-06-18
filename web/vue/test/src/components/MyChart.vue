<template>
<div class="vis">
  {{ spec }}
  here
  <div id="vis"></div>
</div>
</template>

<script>
import embed from 'vega-embed';

export default {
  name: 'MyChart',
  props: {
    spec: Object,
  },
  data: function() {
    return {
    }
  },
  // https://gist.github.com/simonw/7e4b21d0f3cc1d17eaa314fb3f904843 changing data
  // methods: {
  //   getData(){
  //     fetch(this.url, {mode:'cors'}).then(data => data.text()).then(data => {this.data = data;}).catch(err => console.log('Fetch Error :-S', err));
  //   }
  // },
  mounted() {
    // this.data = this.getData();
    embed('#vis', this.spec);
  }
}
</script>
