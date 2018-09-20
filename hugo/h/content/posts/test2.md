---
title: "Chart.js example"
date: 2018-09-20T20:00:12+01:00
draft: false
---

Another post to see Chart.js inclusion working.

<div>
<canvas id="bar-chart-grouped" width="800" height="450"></canvas>
<script>
new Chart(document.getElementById("bar-chart-grouped"), {
    type: 'bar',
    data: {
      labels: ["1900", "1950", "1999", "2050"],
      datasets: [
        {
          label: "Africa",
          backgroundColor: "#3e95cd",
          data: [133,221,783,2478]
        }, {
          label: "Europe",
          backgroundColor: "#8e5ea2",
          data: [408,547,675,734]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Population growth (millions)'
      }
    }
});
</script>
</div>
