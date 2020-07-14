var mobile = false,
	canPostComment = true;

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
	
	$('.like-post img').on('click', function(){
		var post = $(this).closest('.post'),
			id = post.find('.post-id').val();
		
		$.ajax({
			'url': '/like-action/' + id,
			'failure': function(){
				console.log('FAILURE');
			},
			'success': function(data){
				var newImage = post.find('.like-post img').attr('src'), 
					newCount = parseInt(post.find('.like-post p').html());
				
				if (data['following']){
					newImage = newImage.replace('hollow', 'color');
					newCount++;
				} else {
					newImage = newImage.replace('color', 'hollow');
					newCount--;
				}
				
				post.find('.like-post img').attr('src', newImage);
				post.find('.like-post p').html(newCount);
			}
		});
	});
	
	$('.add-comment .field-input').keypress(function(e){
		if (canPostComment && e.which == 13){
			var post = $(this).closest('.post'),
				id = post.find('.post-id').val(),
				commentBox = $(this),
				text = commentBox.val();
			
			canPostComment = false;
			
			console.log("TEST");
			
			$.ajax({
				'url': '/comment',
				'data': {
					'post_id': id,
					'text': text
				},
				'failure': function(){
					canPostComment = true;
					
					commentBox.val('');
				},
				'success': function(data){
					var newComment,
						newCount = parseInt(post.find('.comment-post p').html());
					
					canPostComment = true;
					
					commentBox.val('');
					
					if (post.find('.post-comments').length == 0)
						newComment = $('<div class = "post-comments"><div class = "post-comment"><div class = "comment-image"><p></p></div><div class = "comment-main"><div class = "comment-info"><p class = "comment-name"></p><p class = "comment-posted"></p></div><p class = "comment-text"></p></div></div></div>');
					else
						newComment = post.find('.post-comment').last().clone();
					
					newComment.find('.comment-name').text(data['first_name'] + ' ' + data['last_name']);
					newComment.find('.comment-name').text(data['first_name'] + ' ' + data['last_name']);
					newComment.find('.comment-image p').text(data['first_name'][0]);
					newComment.find('.comment-text').text(text);
					newComment.find('.comment-posted').text('just now');
						
					$(newComment).insertBefore(commentBox.closest('.add-comment'));
					
					newCount++;
					
					post.find('.comment-post p').html(newCount);
					
					console.log(newComment);
				}
			});
		}
	});
});

function markAllRead(div){
	if (div.attr('id') == 'notification-container'){
		div.find('.noti-read').each(function(){
			$(this).addClass('read');
		});
	}
}