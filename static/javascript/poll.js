
// infinite loop
let infinite = new Waypoint.Infinite({
	element: $('.infinite-container')[0],

	offset: 'bottom-in-view',

	onBeforePageLoad: function() {
		$('.loading').removeClass('hidden')
	},

	onAfterPageLoad: function() {
		$('.loading').addClass('hidden')
	}
})