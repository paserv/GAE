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
	$("#meteoit").html("");
	$.post( "meteoit/" + comune + "/" + giorno, function( data ) {
		render_page(data);
		$("#preloader").hide();
		$("#meteoit").show();
	});
}

function render_page(data) {
	$("#meteoitdefs").html(data['svgdefs']);
	var meteoitTable = createTable($("#meteoit"), data['meteoit']);
}

var header = [{"key": "ora", "label": "Ora"},
	  {"key": "svg", "label": ""},
	  {"key": "label", "label": "Previsione"},
	  {"key": "temperatura", "label": "Temperatura"},
	  {"key": "precipitazioni", "label": "Precipitazioni"},
	  {"key": "vento", "label": "Vento"},
	  {"key": "umidita", "label": "Umidita"},
	  {"key": "pressione", "label": "Pressione"}
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
			//if (curr.indexOf('svg')) {
			//	curr = curr.replace('/&lt;', '<');
			//	curr = curr.replace('/&gt;', '>');
			//}
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
         	if (c.indexOf('svg') > 0) {
         		row.append($("<td/>")).append(c);
         	} else {
         		row.append($("<td/>").text(c));
         	}
         });
        body.append(row);
    });
    table.append(body);
    return container.append(table);
}