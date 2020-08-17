$(document).ready(function(){
	$('#store-link').addClass('selected');
	
	$('.sponsor').each(function(){
		$(this).find('.vendor-image-container').css('width', $(this).find('.vendor-image-container').css('height'));
		$(this).find('.vendor-image-container').css('width', $(this).find('.vendor-image-container').css('height'));
	});
});