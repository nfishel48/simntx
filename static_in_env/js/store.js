$(document).ready(function(){
	$('#store-link').addClass('selected');
	
	$('.sponsor .vendor-image-container').each(function(){
		$(this).css('width', $(this).height() + "px");
	});
});