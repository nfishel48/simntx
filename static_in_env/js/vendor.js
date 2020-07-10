$(document).ready(function(){
	$('#follow').on('click', function(){
		var following = $(this).hasClass('following'),
			slug = $('#vendor-slug').val(),
			button = $(this);
		
		$.ajax({
			'url': '/follow-action/' + slug,
			'type': 'POST',
			'failure': function(data){
				console.log('FAIL');
			},
			'success': function(data){
				console.log(following);
				
				if (following){
					button.removeClass('following');
					button.html('Follow');
					
					var count = parseInt($('#follower-count').text()) - 1;
					
					$('#follower-count').text(count);
				} else {
					button.addClass('following');
					button.html('Following');
					
					var count = parseInt($('#follower-count').text()) + 1;
					
					$('#follower-count').text(count);
				}
			},
		});
	});
});