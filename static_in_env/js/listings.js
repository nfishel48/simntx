$(document).ready(function(){
	$('.slide-left').on('click', function(){
		$(this).siblings('.slider').css('margin-left', '0');
		
		$(this).siblings('.slide-right').css('display', 'flex');
		$(this).css('display', 'none');
	});
	$('.slide-right').on('click', function(){
		var outer = $(this).parent().parent().width(),
			inner = $(this).siblings('.slider').width();
		
		var width = inner - outer;
		
		$(this).siblings('.slider').css('margin-left', (0 - width) + 'px');
		
		$(this).siblings('.slide-left').css('display', 'flex');
		$(this).css('display', 'none');
	});
	
	$('.move-left').on('click', function(){
		$(this).parent().parent().parent().find('.slider').css('margin-left', '0');
		
		$(this).siblings('.move-right').css('opacity', '1');
		$(this).css('opacity', '.5');
	});
	$('.move-right').on('click', function(){
		var outer = $(this).parent().parent().parent().find('.section-slide').width(),
			inner = $(this).parent().parent().parent().find('.slider').width();
		
		var width = inner - outer;
		
		console.log($(this).parent().parent().parent().find('.section-slide').width());
		
		$(this).parent().parent().parent().find('.slider').css('margin-left', (0 - width) + 'px');
		
		$(this).siblings('.move-left').css('opacity', '1');
		$(this).css('opacity', '.5');
	});
});