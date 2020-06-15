<template>
</template>

<script>
import embed from 'vega-embed';

export default {
  name: 'MyChart',
  props: {
    spec: Object,
    url: String
  },
  data: function() {
    return {
            data: '',
        },
  methods: {
    getData(){
      fetch(this.url, {mode:'cors'}).then(data => data.json()).then(data => {this.data = data;}).catch(err => console.log('Fetch Error :-S', err));
    }
  },
  mounted() {
    this.data = this.getData();
  }
}
</script>
