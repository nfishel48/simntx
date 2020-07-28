var index = 1,
	adsLoaded;

$(document).ready(function(){
	$('#feed-link').addClass('selected');
	
	$('#load-more-posts').on('click', function(){
		$.ajax({
			'url': '/get_feed_posts',
			'data': {
				'index': index
			},
			'type': 'GET',
			'failure': function(data){
				
			},
			'success': function(data){
				for (var i = 0; i < data['posts'].length; i++){
					$('#feed-posts').append(data['posts'][i]);
				}
				
				if (!data['more_to_load']){
					$('#load-more-posts').remove();
					
					$('#end-of-posts').css('display', 'block');
				}
				
				index++;
			},
		});
	});
});