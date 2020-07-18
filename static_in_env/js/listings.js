var sliderStrength = 1.2;

$(document).ready(function(){
	$('.product-row').each(function(){
		var outerDiv = $(this).find('.slider-container'),
			innerDiv = $(this).find('.slider');
			
		var outer = outerDiv.width(),
			inner = innerDiv.width();
			
		console.log(outer + " // " + inner);
			
		if (inner - outer > 0){
			$(this).find('.slide-right').css('display', 'flex');
		}
	});
	
	$('.slide-left').on('click', function(){
		var sliderContainer = $(this).closest('.product-row').find('.slider-container'),
			slider = $(this).closest('.product-row').find('.slider'),
			left = parseInt(slider.css('margin-left').slice(0, -2)) + sliderContainer.width() / 2 * sliderStrength;
		
		if (left > 0){
			left = 0;
			
			$(this).css('display', 'none');
		}
		
		slider.css('margin-left', left + 'px');
		
		$(this).siblings('.slide-right').css('display', 'flex');
	});
	$('.slide-right').on('click', function(){
		var sliderContainer = $(this).closest('.product-row').find('.slider-container'),
			slider = $(this).closest('.product-row').find('.slider'),
			left = parseInt(slider.css('margin-left').slice(0, -2)) - sliderContainer.width() / 2 * sliderStrength;
		
		var outer = sliderContainer.width(),
			inner = slider.width();
		
		var width = inner - outer;
		
		if (left < -width){
			left = -width;
			
			$(this).css('display', 'none');
		}
		
		slider.css('margin-left', left + 'px');
		
		$(this).siblings('.slide-left').css('display', 'flex');
	});
});