$(window).load(function(){
	// Switch toggle
	var estad0=$('input:checkbox[name=estado]').is(':checked');
	//$("#marcarCasilla").prop('checked',estad0);
	if(estad0==true){
		$(".Switch").removeClass("Off");
		$(".Switch").addClass("On");
	} else {
		$(".Switch").removeClass("On");
		$(".Switch").addClass("Off");
	}

	var activado=estad0;
	$("#nose").children().click(function(){
		if(activado==true){
			$("#marcarCasilla").prop('checked',false);
			activado=false;
			$(".Switch").removeClass("On");
			$(".Switch").addClass("Off");
		} else {
			$("#marcarCasilla").prop('checked',true);
			activado=true;
			$(".Switch").removeClass("Off");
			$(".Switch").addClass("On");
		}
	});
});
