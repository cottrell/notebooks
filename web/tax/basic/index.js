Vue.component('allocation-input', {
	props: ['nothing'],
	computed: {
		allocations: {
			get: function() {
				while (this.internal_allocations.length < this.periods) {
					this.internal_allocations.push(0.5)
				}
				return this.internal_allocations.slice(0, this.periods)
			} 
		}
	},
	data: function() {
		return {
			periods: 3,
			mean_gross: 200000,
			initial_room: 0,
			internal_allocations: [0.5, 0.5, 0.5]
		}
	},
	methods: {
	},
	template: `
	<div class="container">
	<div class="row">
	<p>
	<input v-model.number="periods" type="number"></input> &nbsp periods</br>
	<input v-model.number="mean_gross" type="number"></input> &nbsp mean gross</br>
	<input v-model.number="initial_room" type="number"></input> &nbsp initial room</br>
	 </p>
	</div>
	<p> {{ internal_allocations }} </p>
	<p> {{ allocations }} </p>
	<div class="row" v-for="year in periods">
		<input type="range" min=0 max=1 step=0.01 v-model.number="internal_allocations[year]"></input> &nbsp year {{ year }} allocation
	</div>
	</div>
	`
})

function PiecewiseConstant(xs, ys) {
  return function(x) {
    var lo = 0, hi = xs.length - 1;
    // bisection
    while (hi - lo > 1) {
      var mid = (lo + hi) >> 1;
      if (x < xs[mid]) hi = mid;
      else lo = mid;
    }
    return lo
  };
}

function PiecewiseLinear(xs, ys) {
  return function(x) {
    var lo = 0, hi = xs.length - 1;
    // bisection
    while (hi - lo > 1) {
      var mid = (lo + hi) >> 1;
      if (x < xs[mid]) hi = mid;
      else lo = mid;
    }
    return ys[lo] + (ys[hi] - ys[lo]) / (xs[hi] - xs[lo]) * (x - xs[lo]);
  };
}

var app = new Vue({
	el: "#app",
	data: {
		message: 'Hello Vue!',
		data: []
	},
	computed: {
		reversedMessage: function () {
			return this.message.split('').reverse().join('')
		}
	},
	mounted () {
        // $.getJSON('http://ilikecoding.net/membership/api/memberships', json => {
        $.getJSON('http://raw.githubusercontent.com/cottrell/notebooks/master/data/tax/taxinfo.json', json => {
          this.data = _.filter(json, {'country': 'uk', 'year': '2018-2019'})[0]
          console.log(json)
        })
      }
})

