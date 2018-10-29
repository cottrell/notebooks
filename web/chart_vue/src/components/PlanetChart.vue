<template>
    <div v-bind:class="chartid" >
        <h1>{{ msg }}</h1>
        <canvas id="planet-chart"></canvas>
        ruh oh
    </div>
</template>

<script>
import Chart from 'chart.js';
import planetChartData from './chart-data.js';
export default {
    name: 'adsfasdfasdf', // seems not relevant
    props: {
        msg: String,
        chartid: String
    },
    data () {
        return {
            planetChartData: planetChartData,

        }
    },
    methods: {
        createChart(chartId, chartData) {
            const ctx = document.getElementById(chartId);
            const myChart = new Chart(ctx, {
                type: chartData.type,
                data: chartData.data,
                options: chartData.options,
            });
            return myChart // don't strictly need but eslint complains unused if not returned
        }
    },
    mounted() {
        this.createChart('planet-chart', this.planetChartData);
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
