$(document).ready(function(){
	$(document).on('click', ':not(.nav-button):not(.dropdown-container)', function(){
		console.log('close');
		
		$('.nav-button').each(function(){
			markAllRead($(this));
			
			$(this).find('.dropdown-container').css('display', 'none');
			$(this).removeClass('open');
		});
	});
	
	$('.nav-button').on('click', function(e){
		if ($(e.target).attr('class') == 'dropdown-container' || $(e.target).closest('.dropdown-container').length > 0)
			return;
		
		e.stopPropagation();
		
		$(this).siblings().each(function(){
			$(this).find('.dropdown-container').css('display', 'none');
		});
		
		if ($(this).find('.dropdown-container').css('display') == 'none'){
			$(this).find('.dropdown-container').css('display', 'flex');
			$(this).addClass('open');
		} else {
			$(this).find('.dropdown-container').css('display', 'none');
			$(this).removeClass('open');
			
			markAllRead($(this));
		}
	});
	
	$('#logout-form').on('click', function(){
		$(this).submit();
	});
});

function markAllRead(div){
	if (div.attr('id') == 'notification-container'){
		div.find('.noti-read').each(function(){
			$(this).addClass('read');
		});
	}
}