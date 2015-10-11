$(function() {

	$('.coverflow').coverflow({
		density: 3,
		index: 10, 
		enableWheel: false,
		width: 300,
		height: 445,
		visible: 'density',
		selectedCss:	{	opacity: 1	},
		outerCss:		{	opacity: .1	}
	});

	

});


$(document).ready(function() {
	/*
	 *  Simple image gallery. Uses default settings
	 */

	$('.fancybox').fancybox();
});