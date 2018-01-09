function populate_list() {
	$('input.autocomplete').autocomplete({
		data: get_comuni(),
		limit: 10,
		onAutocomplete: function(val) {
			var comune = $("#search").val().split('(')[0].trim();
			var giorno = $("#rowhome").find(".selected").attr('id');
			render_page(comune, giorno);
		},
		minLength: 1,
	});
}

function find(){
	var comune = $("#search").val().split('(')[0].trim();
	if (comune != "") {
		var giorno = $("#rowhome").find(".selected").attr('id');
		render_page(comune, giorno);
	} else {
		Materialize.toast("Scegli il Comune", 3000);
		$("#preloader").hide();
	}
}

function render_page(comune, giorno) {
	setCookies();
	hideResult();
	
	var fromHour = 0;
	if (giorno == "0") {
		fromHour = getHour();
	}
	
	//createTable("sintesi", fromHour);
	$("input:checkbox[name=prev_type]:checked").each(function () {
		createTable($(this).val(), fromHour);
	});
	
	
	
	$("input:checkbox[name=source_site]:checked").each(function () {
        var source_site = $(this).val();
        $.post( source_site + "/" + comune + "/" + giorno, function( data ) {
	       	updateTables(data, source_site);
	      	$("[id*=" + source_site + "_span]").each(function() {
	       		$(this).show();
	    	});
	       	$("[id*=" + source_site + "_preloader]").each(function() {
	       		$(this).hide();
	    	});
	       	showResult();
    	});
    });
}

function showResult() {
	$("#result").show();
	$("#preloader").hide();
}

function hideResult() {
	$("#preloader").show();
	$("#result").hide();
	$("li[id$=li]").each(function () {
		$(this).hide();
	});	
}

function updateTables(data, site) {
	var myData = data[site];
	$.each(myData, function(index, value) { 
    	var idx = value["ora"].substring(0, 2);
		$("#sintesi_" + site + "_" + idx).html(format(value));
    });
	
	
}
