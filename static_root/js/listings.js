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
		$(this).closest('.product-row').find('.slider').css('margin-left', '0');
		
		$(this).siblings('.slide-right').css('display', 'flex');
		$(this).css('display', 'none');
	});
	$('.slide-right').on('click', function(){
		var outerDiv = $(this).closest('.product-row').find('.slider-container'),
			innerDiv = $(this).closest('.product-row').find('.slider');
		
		var outer = outerDiv.width(),
			inner = innerDiv.width();
		
		var width = inner - outer;
		
		console.log($(outerDiv).width());
		console.log($(innerDiv).width());
		
		$(innerDiv).css('margin-left', (0 - width) + 'px');
		
		$(this).siblings('.slide-left').css('display', 'flex');
		$(this).css('display', 'none');
	});
});