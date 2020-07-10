var mobile = false;

$(document).ready(function(){
	if ($('#search').css('display') == 'none'){
		mobile = true;
		
		$('#search').addClass('closed');
		
		$('#left-panel').css('transition', 'unset');
		toggleLeftPanel();
		
		setTimeout(function(){
			$('#left-panel').css('transition', 'all .3s ease');
		}, 50);
	}
	
	$(document).on('click', function(e){
		if (!$(e.target).is('.nav-button, .dropdown-container, .nav-button *')){
			console.log("NOT DROPDOWN");
			
			$('.nav-button').each(function(){
				markAllRead($(this));
				
				$(this).find('.dropdown-container').css('display', 'none');
				$(this).removeClass('open');
			});
		}
		
		if (mobile){
			if (!$(e.target).is('#nav #search-bar, #nav #search-bar *')){
				console.log("NOT SEARCH BAR");
				
				$('#search').addClass('closed');
				
				$('#search-form').removeClass('closed');
				$('#search-bar').removeClass('closed');
				$('#nav-left').removeClass('closed');
				$('#nav-second-panel').removeClass('closed');
			} else if ($(e.target).is('#nav #search-icon, #nav #search-icon *')){
				console.log("IS SEARCH ICON");
				
				if ($('#search').hasClass('closed')){
					$('#search').removeClass('closed');
					
					$('#search-form').addClass('closed');
					$('#search-bar').addClass('closed');
					$('#nav-left').addClass('closed');
					$('#nav-second-panel').addClass('closed');
				} else {
					$('#search').addClass('closed');
					
					$('#search-form').removeClass('closed');
					$('#search-bar').removeClass('closed');
					$('#nav-left').removeClass('closed');
					$('#nav-second-panel').removeClass('closed');
				}
			}
		}
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