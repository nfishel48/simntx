$(document).ready(function(){
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
});