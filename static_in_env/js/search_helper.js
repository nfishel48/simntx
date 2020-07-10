$(document).ready(function(){
	$('#filters-container input').on('click', function(){
		if ($(this).attr('type') == 'radio'){
			if ($(this).is(".checked")){
				$(this).prop("checked",false).removeClass("checked");
			} else {
				$("input:radio[name='" + $(this).prop("name") + "'].checked").removeClass("checked");
				$(this).addClass("checked");
			}
		}
		
		$('#' + $(this).attr('form')).submit();
	});
	
	$('#page-back-one').on('click', function(e){
		if ($(this).hasClass('disabled'))
			return;
		
		$('#forward-one-input').remove();
		$('#' + $(this).find('input').attr('form')).submit();
		
		console.log($(this));
	});
	$('#page-forward-one').on('click', function(e){
		if ($(this).hasClass('disabled'))
			return;
		
		$('#back-one-input').remove();
		$('#' + $(this).find('input').attr('form')).submit();
	});
	
	$('.page-number').on('click', function(){
		$('#forward-one-input').remove();
		$('#back-one-input').remove();
	});
});