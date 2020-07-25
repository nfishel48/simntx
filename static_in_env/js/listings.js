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
		var sliderContainer = $(this).siblings('.slider-container'),
			slider = sliderContainer.find('.slider'),
			left;
		
		if ($(this).siblings('.slider-container').hasClass('indexed'))
			left = $(this).siblings('.slider-container').width();
		else
			left = parseInt(slider.css('margin-left').slice(0, -2)) + sliderContainer.width() / 2 * sliderStrength;
		
		if (left > 0){
			left = 0;
			
			$(this).css('display', 'none');
		}
		
		slider.css('margin-left', left + 'px');
		
		$(this).siblings('.slide-right').css('display', 'flex');
	});
	$('.slide-right').on('click', function(){
		var sliderContainer = $(this).siblings('.slider-container'),
			slider = sliderContainer.find('.slider'),
			left;
		
		var outer = sliderContainer.width(),
			inner = slider.width();
		
		var width = inner - outer;
		
		if ($(this).siblings('.slider-container').hasClass('indexed'))
			left = -$(this).siblings('.slider-container').width();
		else
			left = parseInt(slider.css('margin-left').slice(0, -2)) - sliderContainer.width() / 2 * sliderStrength;
		
		if (left <= -width){
			left = -width;
			
			$(this).css('display', 'none');
		}
		
		slider.css('margin-left', left + 'px');
		
		$(this).siblings('.slide-left').css('display', 'flex');
	});
	
	$(window).resize(windowResize);
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