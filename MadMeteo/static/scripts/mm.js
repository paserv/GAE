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
	
	var firstCheck = $("input:checkbox[name=prev_type]:checked:first").val();
	var liIndex = $("#table_" + firstCheck + "_li").index();
	$('.collapsible').collapsible('open', liIndex);
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
		$("#precipitazioni_" + site + "_" + idx).html(value["precipitazioni"]);
		$("#temperatura_" + site + "_" + idx).html(value["temperatura"]);
		$("#umidita_" + site + "_" + idx).html(value["umidita"]);
		$("#pressione_" + site + "_" + idx).html(value["pressione"]);
		$("#vento_" + site + "_" + idx).html(value["vento"]);
		$("#neve_" + site + "_" + idx).html(value["neve"]);
		$("#mare_" + site + "_" + idx).html(value["mare"]);
		$("#uv_" + site + "_" + idx).html(value["uv"]);
    });
	
	
}
