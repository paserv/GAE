var anagraficaGiocatori = {}
var counter = 0;
var redazioni = 4;

function populate_players() {
	$.get( "get_players", function( players ) {
		$("#preloader").hide();
		$("#addplayer").show();
		anagraficaGiocatori = players;
		autocompleteData = {};
		$.each(anagraficaGiocatori, function (i, v) {
			autocompleteData[v['playerLabel']] = v['teamUrl'];
		});
		$('input.autocomplete').autocomplete({
		    data: autocompleteData,
		    limit: 10, // The max amount of results that can be shown at once. Default: Infinity.
		    onAutocomplete: function(val) {
		    	var playerName = val.split('(')[0].trim();
		    	var playerId = anagraficaGiocatori[playerName]['id'];
		    	if ($("[id='" + playerId + "']").length) {
		    		Materialize.toast("Giocatore presente", 3000);
		    	} else {
		    		var playermImgURL = anagraficaGiocatori[playerName]['iconUrl'];
		    		var teamImgURL = anagraficaGiocatori[playerName]['teamUrl'];
		    		var statsUrl = anagraficaGiocatori[playerName]['statsUrl'];
		    		var playerRole = anagraficaGiocatori[playerName]['role'];
		    		var player = {};
			    	player['id'] = playerId;
			    	$("#modalFrame").html("<iframe src='" + statsUrl + "' class='modalStats'></iframe>");
			    	$("#playerName").html("Statistiche " + playerName);
			    	var chip = createSimpleChip(player['id'], playerRole, playermImgURL, playerName, statsUrl, teamImgURL);
			    	$("#players").append(chip);
		    		}
		    	},
		    minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
		  });
	});
}

function remove_player(player) {
	$("[id='" + player['id'] + "']").remove();
}

function creaSquadra() {
	$( "#preloader" ).show();
	$("#save_btn").attr("disabled", true);
	
	teamName = $("#teamName").val();
	var found = false;
	if (teamName) {
		$.get( "get_teams", function( teams ) {
			var userTeams = teams['teams']; 
			for (i = 0; i < userTeams.length; i++) { 
			    currTeam = userTeams[i];
			    if (currTeam == teamName) {
					Materialize.toast("Nome squadra esistente", 3000);
					$( "#preloader" ).hide();
					$("#save_btn").removeAttr("disabled");
					found = true;
				}
			}
			if (!found) {
				saveTeam("cs");
			}
		});
	} else {
		Materialize.toast("Inserisci il nome squadra", 3000);
		$( "#preloader" ).hide();
		$("#save_btn").removeAttr("disabled");
	}	
	
}

function modificaSquadra() {
	teamName = $("#teamName").val();
	if (teamName) {
		$("#preloader_players").show();
		$("#edit_btn").attr("disabled", true);
		 $("#delete_btn").attr("disabled", true);
		saveTeam("ms");
	} else {
		Materialize.toast("Inserisci il nome squadra", 3000);
	}
}

function saveTeam(redirect) {
	var result = {};
	result['teamName'] = $("#teamName").val();
	var teamPlayers = [];
	$( ".player" ).each(function( index ) {
		teamPlayers.push($( this ).attr('id'));
	});
	result['teamPlayers'] = teamPlayers;
	$.ajax({
	  type: "POST",
	  url: 'save_team',
	  contentType : 'application/json',
	  data: JSON.stringify(result),
	  success: function( res, status, xhr ) {
		  Materialize.toast(res, 3000);
		  $("#preloader_players").hide();
		  $( "#preloader" ).hide();
		  $("#save_btn").removeAttr("disabled");
		  $("#edit_btn").removeAttr("disabled");
		  $("#delete_btn").removeAttr("disabled");
	  },
	});
}

function getTeamPlayers() {
	$('#players').html("");
	if($( "#teamName" ).val() != "") {
		var team = $( "#teamName" ).val();
		$("#preloader_players").show();
		$("#delete_btn").attr("disabled", true);
		$("#edit_btn").attr("disabled", true);
		$.get( "get_team_players/" + team, function( data ) {
			var team_players = data['players'];
			var ordered_players = orderPlayers(team_players);
			for (i = 0; i < ordered_players.length; i++) {
				var player = {};
				player['id'] = ordered_players[i]['id'];
				var chip = createSimpleChip(ordered_players[i]['id'], ordered_players[i]['role'], ordered_players[i]['iconUrl'], ordered_players[i]['name'], ordered_players[i]['statsUrl'], ordered_players[i]['teamUrl']);
		    	$("#players").append(chip);
			}
			$("#delete_btn").removeAttr("disabled");
			$("#edit_btn").removeAttr("disabled");
			$("#search").removeAttr("disabled");
			$("#preloader_players").hide();
		});
	} else {
		$("#delete_btn").attr("disabled", true);
		$("#edit_btn").attr("disabled", true);
		clearInput();
		$("#search").attr("disabled", true);
	}
}

function createSimpleChip(id, role, iconUrl, name, statsUrl, teamUrl) {
	var player = {};
	player['id'] = id;
	var chip = 
		"<div class='row player' id='" + id +"'>" +
			"<div class='col s1 " + role + "'>" +
				"<div class='mt30'><strong>" + role + "</strong></div>" + 
			"</div>" +
			"<div class='col s10 indigo h80 lighten-5'>" +
				"<img class='imgcard' src='" + iconUrl + "'>" +
				"<img class='imgcard teamicon' src='" + teamUrl + "'><a class='waves-effect waves-light modal-trigger' onclick='openModal(\"" + name + "\",\"" + statsUrl + "\")'><strong>" + name + "</strong></a>" +
			"</div>" +
			"<div class='col s1 indigo lighten-5'>" +
				"<i class='imgcard material-icons curpoint right' onclick='remove_player(" +  JSON.stringify(player) + ")'>close</i>" +
			"</div>" +
		"</div>";
	return chip;
}

function createTitolariChip(id, role, iconUrl, name, statsUrl, teamUrl, team) {
	var newName = getName(name);
	var myId = newName + "_" + team;
	var chip = 
		"<div class='row player ' id='" + id +"' name='" + newName + "' team='" + team.toLowerCase() + "'>" +
			"<div class='col l1 m1 s1 " + role + "'>" +
				"<div class='mt30'><strong>" + role + "</strong></div>" + 
			"</div>" +
			"<div class='col l5 m5 s11 h80 indigo lighten-5'>" +
				"<img class='imgcard' src='" + iconUrl + "'>" +
				"<img class='imgcard teamicon' src='" + teamUrl + "'><a class='waves-effect waves-light modal-trigger' onclick='openModal(\"" + name + "\",\"" + statsUrl + "\")'><strong>" + name + "</strong></a>" +
			"</div>" +
			"<div class='col l4 m3 s12 center'>" +
				getChip(myId, "Gaz") + getChip(myId, "Fan") + getChip(myId, "Med") + getChip(myId, "Sky") +
			"</div>" +
			"<div id='" + newName + "_match" + "' class='col l2 m3 s12 center'>" +
			"</div>" +
		"</div>";
	return chip;
}

function getChip(id, redazione) {
	var chipId = (id + "_" + redazione).toLowerCase();
	var result = "";
	if (redazione == "Gaz" || redazione == "Fan") {
		result = "<div id='" + chipId + "' class='chip mt3 center' style='text-transform:none'>" + redazione +" <i class='info-glipho material-icons'>info_outline</i></div>";
	} else {
		result = "<div id='" + chipId + "' class='chip mt3 center'>" + redazione +"</div>";
	}
	return result;
}

function getTitolari() {
	counter = 0;
	$( ".chip" ).each(function( index ) {
		$( this ).removeClass( "btn green red curpoint" );
	});
	$( "#preloader" ).show();
	$("#titolari_btn").attr("disabled", true);
	findTitolari();
}

function findTitolari() {
	$.get( "gazzetta/matches", function( giornate ) {
		if (!jQuery.isEmptyObject(giornate)) {
			$( ".player" ).each(function( index ) {
				var team = $( this ).attr('team');
				var name = $( this ).attr('name');
				var match = giornate[team];
				var homeTeam = match['home'].charAt(0).toUpperCase() + match['home'].slice(1);
				var awayTeam = match['away'].charAt(0).toUpperCase() + match['away'].slice(1);
				$("#" + name + "_match").html(homeTeam + " - " + awayTeam);
			});
		}
		getTitolariRedazione("gazzetta", giornate, "gaz");
		getTitolariRedazione("fantagazzetta", giornate, "fan");
		getTitolariRedazione("sky", giornate, "sky");
		getTitolariRedazione("mediaset", giornate, "med");
	}).fail(function() {
		Materialize.toast("Giornata non disponibile", 3000);
		$( "#preloader" ).hide();
	});
}

function getTitolariRedazione(redazione, giornate, shortName) {
	$.ajax({
	    type: 'POST',
	    url: redazione,
	    data: JSON.stringify(giornate),
	    success: function (data) {
	    	var squadre = data;
	    	if (!jQuery.isEmptyObject(squadre)) {
				$( ".player" ).each(function( index ) {
					var team = $( this ).attr('team');
					var name = $( this ).attr('name');
					if (squadre[team]) {
						var titolari = squadre[team]['titolari'];
						var divId = "#" + name + "_" + team + "_" + shortName;
						if (isTitolare(name, titolari)) {
							$(divId).addClass('green');
						} else {
							$(divId).addClass('red');
						}
						if (shortName == 'gaz') {
							$(divId).click(function(){ openModalDetails(squadre[team]['details']); });
							$(divId).addClass('curpoint btn');
						}
						if (shortName == 'fan') {
							$(divId).click(function(){ openModalDetails(squadre[team]['details']); });
							$(divId).addClass('curpoint btn');
						}
					}
				});
			}
	    	counter = counter + 1;
			if (counter == redazioni) {
				$( "#preloader" ).hide();
			    $("#titolari_btn").removeAttr("disabled");
			}
	    },
	    contentType: "application/json",
	    dataType: 'json'
	});
}

function loadTeam() {
	$("#titolari_btn").attr("disabled", true);
	$('#players').html("");
	if($( "#teamName" ).val() != "") {
		$("#preloader_players").show();
		var team = $( "#teamName" ).val();
		$.get( "get_team_players/" + team, function( data ) {
			team_players = data['players'];
			var ordered_players = orderPlayers(team_players);
			for (i = 0; i < ordered_players.length; i++) {
				var player = {};
				player['id'] = ordered_players[i]['id'];
				var chip = createTitolariChip(ordered_players[i]['id'], ordered_players[i]['role'], ordered_players[i]['iconUrl'], ordered_players[i]['name'], ordered_players[i]['statsUrl'], ordered_players[i]['teamUrl'], ordered_players[i]['team']);
		    	$("#players").append(chip);
			}
			$("#preloader_players").hide();
			$("#titolari_btn").removeAttr("disabled");
		});
	} else {
		Materialize.toast("Inserisci il nome squadra", 3000);
	}
}

function deleteTeam() {
	if ($("#teamName").val()) {
		$("#preloader_players").show();
		$("#delete_btn").attr("disabled", true);
		$("#edit_btn").attr("disabled", true);
		var team = $( "#teamName" ).val();
		$.ajax({
		    url: 'delete_team/' + team,
		    type: 'DELETE',
		    success: function(result) {
		    	Materialize.toast(result, 3000);
		    	$("#preloader_players").hide();
		    	window.location.href = "ms";
		    }
		});
	} else {
		Materialize.toast("Inserisci il nome squadra", 3000);
	}	
}

function openModal(name, statsUrl) {
	$("#playerName").html("Statistiche " + name);
	$("#modalFrame").html("<iframe src='" + statsUrl + "' class='modalStats'></iframe>");
	$("#modalStats").modal('open');
}

function openModalDetails(content) {
	$("#modalContent").html(content);
	$("#modalDetails").modal('open');
}

function clearInput() {
	$("#search").val(""); 
}

function orderPlayers(players) {
	result = [];
	$.each(players, function( index, value ) {
		if (value['role'] == 'P') {
			result.push(value);
		}
	});
	$.each(players, function( index, value ) {
		if (value['role'] == 'D') {
			result.push(value);
		}
	});
	$.each(players, function( index, value ) {
		if (value['role'] == 'C') {
			result.push(value);
		}
	});
	$.each(players, function( index, value ) {
		if (value['role'] == 'A') {
			result.push(value);
		}
	});
	return result;
}

function clearTitolari() {
	$( ".player" ).each(function( index ) {
		var team = $( this ).attr('team');
		var name = $( this ).attr('name');
		$("[id^=" + name + "_" + team).removeClass('green');
		$("[id^=" + name + "_" + team).removeClass('red');
		$("[id^=" + name + "_match").html("");
	});
}

function getName(name) {
	var newName = name.replace(" ", "_");
	var splittedSpace = newName.split(" ");
	if (splittedSpace.length > 1) {
		newName = splittedSpace.reduce(function (a, b) { return a.length > b.length ? a : b; });
	}
	var splittedDash = name.split("-");
	if (splittedDash.length > 1) { 
		newName = splittedDash.reduce(function (a, b) { return a.length > b.length ? a : b; });
	}
	var splittedApostr = name.split("'");
	if (splittedApostr.length > 1) { 
		newName = splittedApostr.reduce(function (a, b) { return a.length > b.length ? a : b; });
	}
	return newName.toLowerCase();
}

function isTitolare(name, titolari) {
	var result = false;
	var newName = name;
	var splittedUnderscore = newName.split("_");
	if (splittedUnderscore.length > 1) {
		newName = splittedUnderscore.reduce(function (a, b) { return a.length > b.length ? a : b; });
	}
	$.each(titolari, function( index, value ) {
		if (value.indexOf(newName) >= 0) {
			result = true;
		}
	});
	return result;
}

function submitForm() {
	var input = {};
	if ($("#lega").val() && $("#squadra").val()) {
		$("#preloader").show();
		input['lega'] = $("#lega").val();
		input['squadra'] = $("#squadra").val();
		$.post("import", input, function(data) {
	        Materialize.toast(data, 3000);
	        $("#preloader").hide();
	    });
	} else {
		Materialize.toast("Compila tutti i campi", 3000);
	}

}