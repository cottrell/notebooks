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
			initial_pension_room: 0,
			internal_allocations: [0.5, 0.5, 0.5]
		}
	},
	methods: {
	},
	template: `
	<div class="container">
	<div class="row">
	<input v-model.number="periods" type="number"></input> &nbsp periods
	</div>
	<p> {{ internal_allocations }} </p>
	<p> {{ allocations }} </p>
	<div class="row" v-for="year in periods">
		<input type="range" min=0 max=1 step=0.01 v-model.number="internal_allocations[year]"></input> &nbsp year {{ year }} allocation
	</div>
	</div>
	`
})

var app = new Vue({
	el: "#app",
	data: {
		message: 'Hello Vue!'
	},
	computed: {
		reversedMessage: function () {
			return this.message.split('').reverse().join('')
		}
	}
})

