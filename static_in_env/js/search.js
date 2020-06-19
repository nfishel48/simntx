$(document).ready(function(){
	$('#tags-container .tag').on('click', function(){
		$('#added-tags-container').append($(this));
		$('#added-tags-container').append('<input checked style = "display: none;" type = "checkbox" name = "tags" value = "' + $(this).text().trim() + '">')
		
		$(this).removeClass('hollow');
		$(this).css({'color': 'white', 'background-color': $(this).css('border-color')});
	});
});