$(document).ready(function(){
	$('#left-panel-expand').on('click', function(){
		var leftPanel = $('#left-panel'),
			rightPanel = $('#right-panel');
		
		/*if (leftPanel.hasClass('closed')){
			$(':root').css('--content-container-margin', 'var(--left-panel-width)');
			leftPanel.css('margin-left', '0px');
			
			leftPanel.removeClass('closed');
			$(this).addClass('open');
			
			console.log('now open');
		} else {
			$(':root').css('--content-container-margin', '0');
			leftPanel.css('margin-left', -$('#left-panel').outerWidth() + 'px');
			
			leftPanel.removeClass('open');
			leftPanel.addClass('closed');
			
			console.log('now closed');
		}*/
		
		console.log(parseInt(leftPanel.css('left').slice(0, -2)));
		
		if (parseInt(leftPanel.css('left').slice(0, -2)) == 0){
			$(':root').css('--left-panel-margin', -leftPanel.outerWidth() + 'px');
			//rightPanel.css('margin-left', 0)
		} else {
			$(':root').css('--left-panel-margin', '0px');
			//rightPanel.css('margin-left', leftPanel.outerWidth());
			
			console.log('RESET');
		}
	});
});