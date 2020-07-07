$(document).ready(function(){
	$('#left-panel-expand').on('click', function(){
		var leftPanel = $('#left-panel');
		
		if (parseInt(leftPanel.css('left').slice(0, -2)) == 0){
			$(':root').css('--left-panel-margin', -leftPanel.outerWidth() + 'px');
		} else {
			$(':root').css('--left-panel-margin', '0px');
		}
	});
	
	$('#notification-container').on('click', function(){
		$.ajax({
			url: '/clear-notifications',
		});
		
		$(this).find('.item-count-badge').remove();
	});
});