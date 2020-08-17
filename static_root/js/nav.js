$(document).ready(function(){
	$('#left-panel-expand').on('click', function(){
		toggleLeftPanel();
	});
	
	$('#notification-container').on('click', function(){
		$.ajax({
			url: '/read-notifications',
		});
		
		$(this).find('.item-count-badge').remove();
	});
	
	$('#clear-notifications').on('click', function(){
		$.ajax({
			'url': '/clear-notifications',
			'success': function(){
				console.log('CLEARED NOTIFICATIONS');
				
				$('.notification-container').each(function(){
					$(this).remove();
					
					console.log('noti');
				});
			}
		});
	});
});

function toggleLeftPanel(){
	var leftPanel = $('#left-panel');
		
	if (parseInt(leftPanel.css('left').slice(0, -2)) == 0){
		$(':root').css('--left-panel-margin', -leftPanel.outerWidth() + 'px');
	} else {
		$(':root').css('--left-panel-margin', '0px');
	}
}