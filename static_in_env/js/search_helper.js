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
});