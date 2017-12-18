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
	$("#preloader").show();
	$("#result").html("");
	$("#result").hide();
	
	var numCols = 3;
	var fromHour = 0;
	if (giorno == "0") {
		fromHour = getHour();
	}
	createTable($("#result"), fromHour, numCols);
	
	$.post( "meteoit/" + comune + "/" + giorno, function( data ) {
		updateTable(data, "meteoit");
	});
	$.post( "trebmeteo/" + comune + "/" + giorno, function( data ) {
		updateTable(data, "3bmeteo");
	});
	$("#result").show();
	$("#preloader").hide();
}

function updateTable(data, site) {
	var myData = data[site];
	$.each(myData, function(index, value) { 
    	var idx = value["ora"].substring(0, 2);
		$("#" + site + "_" + idx).html(format(value));
    });
	
	
}

function groupData(data) {
	var result = [];
	result[0] = {"ora": "09:00", "meteoit": "Meteo IT", "3bMeteo": "3bMeteo"};
	result[1] = {"ora": "10:00", "meteoit": "Meteo IT", "3bMeteo": "3bMeteo"};
	result[2] = {"ora": "11:00", "meteoit": "Meteo IT", "3bMeteo": "3bMeteo"};
	result[3] = {"ora": "12:00", "meteoit": "Meteo IT", "3bMeteo": "3bMeteo"};
	result[4] = {"ora": "13:00", "meteoit": "Meteo IT", "3bMeteo": "3bMeteo"};
	
	return result;
}


var header = [{"key": "ora", "label": " "},
	  {"key": "meteoit", "label": "meteoit"},
	  {"key": "3bmeteo", "label": "3bmeteo"},
//	  {"key": "label", "label": "Previsione"},
//	  {"key": "temperatura", "label": "Temperatura"},
//	  {"key": "precipitazioni", "label": "Precipitazioni"},
//	  
//	  {"key": "vento", "label": "Vento"},
//	  {"key": "umidita", "label": "Umidita"},
//	  {"key": "pressione", "label": "Pressione"},
//	  {"key": "uv", "label": "UV"}
	  ];


function createTable(container, fromHour, numcols) {
	var numRows = 24 - fromHour;
	
	var currHeader = [];
	$.each(header, function( headerValIndex, headerVal ) {
		currHeader.push(headerVal['label']);
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
    for (var i = fromHour; i <= 23; i++) {
    	var index = i;
    	if (i < 10) {
    		index = "0" + i;
		}
    	var row = $("<tr/>");
    	row.attr("id", "row_" + index);
    	for (var j = 0; j < numcols; j++) {
    		var col = $("<td/>");
    		col.attr("id", header[j]["key"] + "_" + index);
    		if (j == 0) {
    			col.text(index + ":00");
    		}
    		row.append(col);
    	}
    	body.append(row);
    }
    table.append(body);
    return container.append(table);
}






//function createTable(container, data) {
//	var orderedData = [];
//	
//	var currHeader = [];
//	$.each(header, function( headerValIndex, headerVal ) {
//		currHeader.push(headerVal['label']);
//	});
//	
//	$.each(data, function( dataValIndex, dataVal ) {
//		var currentData = [];
//		$.each(header, function( headerValIndex, headerVal ) {
//			curr = dataVal[headerVal['key']];
//			currentData.push(curr);
//		});
//		orderedData.push(currentData);
//	});
//	
//	
//    var table = $("<table/>").addClass('striped');
//    
//    var head = $("<thead/>");
//    var row = $("<tr/>");
//    $.each(currHeader, function(colIndex, c) { 
//    	row.append($("<th/>").text(c));
//    });
//    head.append(row);
//    table.append(head);
//    
//    var body = $("<tbody/>");
//    $.each(orderedData, function(rowIndex, r) {
//     	var row = $("<tr/>");
//         $.each(r, function(colIndex, c) { 
//       		row.append($("<td/>").text(c));
//         });
//        body.append(row);
//    });
//    table.append(body);
//    return container.append(table);
//}