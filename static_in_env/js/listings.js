$(document).ready(function(){
	$('.slide-left img').on('click', function(){
		$(this).closest('.section').find('.slider').css('margin-left', '0');
		
		$(this).parent().siblings('.slide-right').css('display', 'flex');
		$(this).parent().css('display', 'none');
	});
	$('.slide-right img').on('click', function(){
		var outerDiv = $(this).closest('.section').find('.section-slide'),
			innerDiv = $(this).closest('.section').find('.slider');
		
		var outer = outerDiv.width(),
			inner = innerDiv.width();
		
		var width = inner - outer;
		
		console.log($(outerDiv).width());
		
		$(innerDiv).css('margin-left', (0 - width) + 'px');
		
		$(this).parent().siblings('.slide-left').css('display', 'flex');
		$(this).parent().css('display', 'none');
	});
});