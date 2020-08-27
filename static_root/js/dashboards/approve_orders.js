function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
	
    setInterval(function () {
        if ($('#refresh')[0].checked){
			minutes = parseInt(timer / 60, 10);
			seconds = parseInt(timer % 60, 10);

			minutes = minutes < 10 ? "0" + minutes : minutes;
			seconds = seconds < 10 ? "0" + seconds : seconds;

			display.text(":" + seconds);

			if (--timer < 0) {
				location.reload(true);
			}
		}
    }, 1000);
}

window.onload = function () {
    var time = 59,
        display = $('#refresh-timer');
		
    startTimer(time, display);
};