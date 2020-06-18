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
});