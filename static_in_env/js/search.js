$(document).ready(function(){
	var index = 5;
	
	$(document).on('click', '#tags-container .tag', function(){
		$('#added-tags-container').append('<input checked style = "display: none;" type = "checkbox" name = "tags" value = "' + $(this).text().trim() + '">')
		
		$(this).removeClass('hollow');
		$(this).css({'color': 'white', 'background-color': $(this).css('border-color')});
		
		var temp = $(this)[0].outerHTML;
		$('#added-tags-container').append(temp);
		
		$(this).remove();
	});
	$(document).on('click', '#added-tags-container .tag', function(){
		console.log($(this).text().trim());
		
		$(this).siblings('input[value=' + $(this).text().trim() + ']').remove();
		
		$(this).addClass('hollow');
		$(this).css({'color': $(this).css('border-color'), 'background-color': 'white'});
		
		var temp = $(this)[0].outerHTML;
		$('#tags-container').append(temp);
		
		$(this).remove();
	});
	
	$('#load-more').on('click', function(){
		$.ajax({
			url: '/search_more',
			data: {
				
			},
			error: function(e){
				
			},
			success: function(data) {
				console.log(data);
				
				if (!data['show_load_button']){
					$('#load-more').remove();
				}
				
				for (var i = 0; i < data['product_results'][0].length; i++){
					var new_listing = $(listing_item),
						item = data['product_results'][0][i];
					
					$(new_listing).attr('href', item['url']);
					$(new_listing).find('img').attr('src', item['image_url']);
					$(new_listing).find('.listing-title').text(item['title']);
					$(new_listing).find('.listing-tags').html('');
					
					item['tags'].forEach(function(tag, index){
						$(new_listing).find('.listing-tags').append("<div class = 'tag' style = 'background-color: " + tag[1] + "'>" + tag[0] + "</div>");
					});
					
					if (item['type'] == 'product'){
						$(new_listing).find('.listing-vendor').text(item['vendor']['title']);
						$(new_listing).find('.listing-price').text(item['price']);
					}
					
					$('#listings').append(new_listing);
				}
			}
		});
	});
});