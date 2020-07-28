var mobile = false,
	canPostComment = true;

$(document).ready(function(){
	if ($('.messages').length > 0){
		messagesResize();
	}
	
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
					newComment.find('.comment-image p').text(data['first_name'][0]);
					newComment.find('.comment-text').text(text);
					newComment.find('.comment-posted').text('just now');
					
					if (post.find('.post-comments').length == 0)
						$(newComment).insertBefore(commentBox.closest('.add-comment'));
					else
						$('.post-comments').append(newComment);
					
					newCount++;
					
					post.find('.comment-post p').html(newCount);
					
					console.log(newComment);
				}
			});
		}
	});
	
	$('.follow').on('click', function(){
		var following = $(this).hasClass('following'),
			slug = $(this).parent('.follow-container').find('.vendor-slug').val(),
			button = $(this),
			countDiv = $(this).siblings('.follow-count').find('.follower-count');
		
		if (following){
			button.removeClass('following');
			button.html('Follow');
			
			var count = parseInt(countDiv.text()) - 1;
			
			countDiv.text(count);
		} else {
			button.addClass('following');
			button.html('Following');
			
			var count = parseInt(countDiv.text()) + 1;
			
			countDiv.text(count);
		}
		
		$.ajax({
			'url': '/follow-action/' + slug,
			'type': 'POST',
			'failure': function(data){
				console.log('FAIL');
			},
			'success': function(data){
				console.log(following);
			},
		});
	});
	$('.load-more-comments').on('click', function(){
		var post = $(this).closest('.post'),
			id = post.find('.post-id').val(),
			index = post.find('.comment-index').val();
			
		$.ajax({
			'url': '/comments',
			'data': {
					'post_id': id,
					'index': index
			},
			'type': 'GET',
			'failure': function(data){
				
			},
			'success': function(data){
				console.log(data);
				
				for (var i = 0; i < data['comments'].length; i++){
					var comment = data['comments'][i];
					
					console.log(data['comments'][i]);
					
					var newComment = post.find('.post-comment').last().clone();
					
					newComment.find('.comment-name').text(comment['first_name'] + ' ' + comment['last_name']);
					newComment.find('.comment-image p').text(comment['first_name'][0]);
					newComment.find('.comment-text').text(comment['text']);
					newComment.find('.comment-posted').text(comment['posted']);
					
					post.find('.post-comments').prepend(newComment);
				}
				
				if (!data['more_to_load'])
					$('.load-more-comments').remove();
				else
					post.find('.comment-index').val(parseInt(post.find('.comment-index').val()) + 1);
			},
		});
	});
	
	$('.message .close').on('click', function(){
		$(this).parent('.message').remove();
		
		messagesResize();
	});
});

function markAllRead(div){
	if (div.attr('id') == 'notification-container'){
		div.find('.noti-read').each(function(){
			$(this).addClass('read');
		});
	}
}

function messagesResize(){
	$('#container').css('margin-top', $('.messages').height() + 'px');
	$('#left-panel').css('top', $('.messages').height() + 'px');
}