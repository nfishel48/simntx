var sliderStrength = 1.2;

$(document).ready(function(){
	windowResize();
	
	$('.slider-container').each(function(){
		var outerDiv = $(this),
			innerDiv = outerDiv.find('.slider');
			
		var outer = outerDiv.width(),
			inner = innerDiv.width();
			
		if (inner - outer > 0){
			outerDiv.siblings('.slide-right').css('display', 'flex');
			
			console.log(outerDiv.siblings('.slide-right').css('display'));
		} else {
			console.log(outer + ' // ' + inner);
		}
	});
	
	$('.slide-left').on('click', function(){
		slideSponsors($(this).siblings('.slider-container'), true);
	});
	$('.slide-right').on('click', function(){
		slideSponsors($(this).siblings('.slider-container'), false);
	});
	
	$(window).resize(windowResize);
	
	if ($('#sponsored-vendors .slider').children().length > 1){
		var timer = new IntervalTimer(function(){
			slideSponsors($('#sponsored-vendors .slider-container'));
		}, 7500);
	}
	
	$('#sponsored-vendors').on('mouseenter', function(){
		timer.pause();
	});
	$('#sponsored-vendors').on('mouseleave', function(){
		timer.resume();
	});
});

function windowResize(){
	$('.sponsor').each(function(){
		$(this).width($('#sponsored-vendors').width() + "px");
	});
	
	$('.listing-item').each(function(){
		var imageContainer = $(this).find('.listing-image-container')
		
		if ($(this).parent('.products-container').length > 0)
			$(this).height($(this).width() + 'px');
		
		imageContainer.css('width', imageContainer.height() + "px");
	});
}

function slideSponsors(sliderContainer, left){
	var slider = sliderContainer.find('.slider'),
		slideLeft = sliderContainer.siblings('.slide-left'),
		slideRight = sliderContainer.siblings('.slide-right'),
		leftMargin = parseInt(slider.css('margin-left').slice(0, -2)),
		outer = sliderContainer.width(),
		inner = slider.width(),
		width = inner - outer,
		indexed = sliderContainer.hasClass('indexed');
	
	if (indexed)
		leftMargin += sliderContainer.width() * (left ? 1 : -1);
	else
		leftMargin += sliderContainer.width() * (left ? 1 : -1) / 2 * sliderStrength;

	console.log(outer + ' // ' + inner);
	console.log('LEFT MARGIN: ' + leftMargin + ' // WIDTH: ' + width);

	if (leftMargin > 0){
		leftMargin = 0;
		
		slideLeft.css('display', 'none');
	} else if (leftMargin < -width){
		if (indexed)
			leftMargin = 0;
		else {
			leftMargin = -width;
		
			slideRight.css('display', 'none');
		}
	}
	
	slider.css('margin-left', leftMargin + 'px');
	
	if (left)
		slideRight.css('display', 'flex');
	else
		slideLeft.css('display', 'flex');
}

 function IntervalTimer(callback, interval) {
	var timerId, startTime, remaining = 0;
	var state = 0; //  0 = idle, 1 = running, 2 = paused, 3= resumed

	this.pause = function () {
		if (state != 1) return;

		remaining = interval - (new Date() - startTime);
		window.clearInterval(timerId);
		state = 2;
	};

	this.resume = function () {
		if (state != 2) return;

		state = 3;
		window.setTimeout(this.timeoutCallback, remaining);
	};

	this.timeoutCallback = function () {
		if (state != 3) return;

		callback();

		startTime = new Date();
		timerId = window.setInterval(callback, interval);
		state = 1;
	};

	startTime = new Date();
	timerId = window.setInterval(callback, interval);
	state = 1;
}