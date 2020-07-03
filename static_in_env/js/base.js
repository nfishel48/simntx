$(document).ready(function(){
	$(document).on('click', ':not(.nav-button):not(.dropdown-container)', function(){
		console.log('close');
		
		$('.nav-button').each(function(){
			$(this).find('.dropdown-container').css('display', 'none');
		});
	});
	
	$('.nav-button').on('click', function(e){
		e.stopPropagation();
		
		if ($(e.target).attr('class') == 'dropdown-container' || $(e.target).closest('.dropdown-container').length > 0)
			return;
		
		$(this).siblings().each(function(){
			$(this).find('.dropdown-container').css('display', 'none');
		});
		
		if ($(this).find('.dropdown-container').css('display') == 'none')
			$(this).find('.dropdown-container').css('display', 'flex');
		else
			$(this).find('.dropdown-container').css('display', 'none');
	});
	
	$('#logout-form').on('click', function(){
		$(this).submit();
	});
});