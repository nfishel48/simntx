$(document).ready(function(){
	/*$(document).on('click', function(){
		$('.dropdown ul').css('display', 'none');
	});
	
	$('.dropdown').on('click', function(e){
		e.stopPropagation();
		
		console.log("HELLO");
	
		if ($(this).find('ul').css('display') == 'block'){
			$(this).find('ul').css('display', 'none');
		} else {
			$(this).find('ul').css('display', 'block');
		}
	});
	
	$('.dropdown ul li').on('click', function(){
		var label = $(this).text();
		
		$(this).parent().siblings('p').text(label);
		
		var before = $(this).prev();
		
		$(this).siblings().eq(0).before($(this));
		$(before).after($(this).siblings().eq(0));
	});
	
	fixDropdownWidth();*/
	
	$('.slide-left').on('click', function(){
		$(this).siblings('.slider').css('margin-left', '0');
		
		$(this).siblings('.slide-right').css('display', 'flex');
		$(this).css('display', 'none');
	});
	$('.slide-right').on('click', function(){
		var outer = $(this).parent().parent().width(),
			inner = $(this).siblings('.slider').width();
		
		var width = inner - outer;
		
		$(this).siblings('.slider').css('margin-left', (0 - width) + 'px');
		
		$(this).siblings('.slide-left').css('display', 'flex');
		$(this).css('display', 'none');
	});
});

function fixDropdownWidth(){
	$('.dropdown').each(function(){
		var width = parseInt($(this).find('img').width()) + parseInt($(this).find('img').css('margin-left')[0]);
		console.log('0 ' + (20 + width) + 'px !important');
		
		//$(this).find('li').css('padding', '0 ' + (15 + width) + 'px');
		$(this).width($(this).children('ul').outerWidth());
	});
}