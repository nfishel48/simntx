$(document).ready(function(){
	$('.promotion-choice').on('click', function(){
		$('#promotion-choices').css('display', 'none');
		$('#promotion-choose').css('display', 'none');
		
		$('.promotion-option').eq($(this).index()).css('display', 'flex');
	});
	
	$('.promotion-option .limited option').on('click', function(){
		var selected = 0;
		
		if ($(this)[0].selected){
			selected++;
			
			$(this).siblings('option:checked').each(function(){
				selected++;
			});
			
			if (selected > 5)
				$(this)[0].selected = false;
		}
	});
});