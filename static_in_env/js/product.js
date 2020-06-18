$(document).ready(function(){
	$('.selector-image').on('click', function(){
		var index = $(this).index();
		
		$(this).siblings().each(function(){
			$(this).removeClass('selected');
		});
		
		$(this).addClass('selected');
		
		$('#gallery-image').children().each(function(){
			$(this).css('display', 'none');
		});
		
		$('#gallery-image').children().eq(index).css('display', 'block');
	});
});