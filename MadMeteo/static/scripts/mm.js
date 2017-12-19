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
	clearData();//$("#result").html("");
	$("#result").hide();
	
	var numCols = 3;
	var fromHour = 0;
	if (giorno == "0") {
		fromHour = getHour();
	}
	
	createTable($("#table_sintesi"), fromHour, numCols);
	
	$.post( "meteoit/" + comune + "/" + giorno, function( data ) {
		updateTable(data, "meteoit");
		$("#meteoit_head").html("Meteo.it");
		$("#result").show();
		$("#preloader").hide();
	});
	$.post( "trebmeteo/" + comune + "/" + giorno, function( data ) {
		updateTable(data, "3bmeteo");
		$("#3bmeteo_head").html("3BMeteo");
		$("#result").show();
		$("#preloader").hide();
	});
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