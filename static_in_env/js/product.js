$(document).ready(function(){
	var index = 0;
	
	console.log(index);
	
	$('.gallery-img').each(function(){
		$(this).css({/*'background-color': randomColor(), */'width': $(this).parent().parent().css('width')});
	});
	
	for(var i = 0; i < $('#gallery').children().length; i++){
		$('#gallery-index').append('<div class = "gallery-circle"></div>')
	}
	
	$('#gallery-index').children().eq(index).addClass('selected');
	
	$('.gallery-button').on('click', function(){
		if ($(this).hasClass('left')){
			if (index == 0){
				index = $('#gallery-images').children().length - 1;
			} else {
				index--;
			}
		} else {
			if (index == $('#gallery-images').children().length - 1){
				index = 0;
			} else {
				index++;
			}
		}
		
		$('#gallery-images').css('margin-left', -index * Math.ceil(parseInt($('.gallery-img').css('width'))));
		
		$('#gallery-index').children().eq(index).addClass('selected').siblings().removeClass('selected');
	});
	
	$('.gallery-circle').on('click', function(){
		index = $(this).index();
		
		$('#gallery-images').css('margin-left', -index * Math.ceil(parseInt($('.gallery-img').css('width'))));
		
		$('#gallery-index').children().eq(index).addClass('selected').siblings().removeClass('selected');
	});
});