var site_to_query = 2;

function populate_list() {
	$('input.autocomplete').autocomplete({
		data: get_comuni(),
		limit: 10,
		onAutocomplete: function(val) {
			var comune = $("#search").val().split('(')[0].trim();
			var giorno = $("#rowhome").find(".selected").attr('id');
			findByComuneAndDay(comune, giorno);
		},
		minLength: 1,
	});
}

function find(){
	var comune = $("#search").val().split('(')[0].trim();
	if (comune != "") {
		var giorno = $("#rowhome").find(".selected").attr('id');
		findByComuneAndDay(comune, giorno);
	} else {
		Materialize.toast("Scegli il Comune", 3000);
	}
	
}

function findByComuneAndDay(comune, giorno) {
	$("#preloader").show();
	$("#result").html("");
	$("#result").hide();
	queried_sites = 0;
	$.post( "meteoit/" + comune + "/" + giorno, function( data ) {
		queried_sites = queried_sites + 1;
		if (site_to_query == queried_sites) {
			render_page(data);
		}
	});
	$.post( "trebmeteo/" + comune + "/" + giorno, function( data ) {
		queried_sites = queried_sites + 1;
		if (site_to_query == queried_sites) {
			render_page(data);
		}
	});
}

function render_page(data) {
	mergeData = {};
	mergeData['meteoit'] = [];
	
	
	var meteoitTable = createTable($("#result"), data['3bmeteo']);
	$("#preloader").hide();
	$("#result").show();
}

var header = [{"key": "ora", "label": " "},
	  {"key": "Meteo.it", "label": "meteoit"},
	  {"key": "3BMeteo", "label": "3bmeteo"},
//	  {"key": "label", "label": "Previsione"},
//	  {"key": "temperatura", "label": "Temperatura"},
//	  {"key": "precipitazioni", "label": "Precipitazioni"},
//	  
//	  {"key": "vento", "label": "Vento"},
//	  {"key": "umidita", "label": "Umidita"},
//	  {"key": "pressione", "label": "Pressione"},
//	  {"key": "uv", "label": "UV"}
	  ];

function createTable(container, data) {
	var orderedData = [];
	
	var currHeader = [];
	$.each(header, function( headerValIndex, headerVal ) {
		currHeader.push(headerVal['label']);
	});
	
	$.each(data, function( dataValIndex, dataVal ) {
		var currentData = [];
		$.each(header, function( headerValIndex, headerVal ) {
			curr = dataVal[headerVal['key']];
			currentData.push(curr);
		});
		orderedData.push(currentData);
	});
	
	
    var table = $("<table/>").addClass('striped');
    
    var head = $("<thead/>");
    var row = $("<tr/>");
    $.each(currHeader, function(colIndex, c) { 
    	row.append($("<th/>").text(c));
    });
    head.append(row);
    table.append(head);
    
    var body = $("<tbody/>");
    $.each(orderedData, function(rowIndex, r) {
     	var row = $("<tr/>");
         $.each(r, function(colIndex, c) { 
       		row.append($("<td/>").text(c));
         });
        body.append(row);
    });
    table.append(body);
    return container.append(table);
}