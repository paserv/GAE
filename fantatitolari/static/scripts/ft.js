var anagraficaGiocatori = {}
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
		    limit: 20, // The max amount of results that can be shown at once. Default: Infinity.
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
	teamName = $("#teamName").val();
	var found = false;
	if (teamName) {
		$.get( "get_teams", function( teams ) {
			var userTeams = teams['teams']; 
			for (i = 0; i < userTeams.length; i++) { 
			    currTeam = userTeams[i];
			    if (currTeam == teamName) {
					Materialize.toast("Nome squadra esistente", 3000);
					found = true;
				}
			}
			if (!found) {
				saveTeam("cs");
			}
		});
	} else {
		Materialize.toast("Inserisci il nome squadra", 3000);
	}	
	
}

function modificaSquadra() {
	teamName = $("#teamName").val();
	if (teamName) {
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
	  },
	});
}

function getTeamPlayers() {
	$('#players').html("");
	if($( "#teamName" ).val() != "") {
		var team = $( "#teamName" ).val();
		$.get( "get_team_players/" + team, function( data ) {
			var team_players = data['players'];
			var ordered_players = orderPlayers(team_players);
			for (i = 0; i < ordered_players.length; i++) {
				var player = {};
				player['id'] = ordered_players[i]['id'];
				var chip = createSimpleChip(ordered_players[i]['id'], ordered_players[i]['role'], ordered_players[i]['iconUrl'], ordered_players[i]['name'], ordered_players[i]['statsUrl'], ordered_players[i]['teamUrl']);
		    	$("#players").append(chip);
			}
		});
		$("#delete_btn").removeAttr("disabled");
		$("#edit_btn").removeAttr("disabled");
		$("#search").removeAttr("disabled");
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
			"<div class='col s1 " + role + "' style='width:auto'>" +
				"<div class='mt30'><strong>" + role + "</strong></div>" + 
			"</div>" +
			"<div class='col s10 indigo lighten-5'>" +
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
	var myId = name + "_" + team;
	var chip = 
		"<div class='row player ' id='" + id +"' name='" + name.toLowerCase() + "' team='" + team.toLowerCase() + "'>" +
			"<div class='col l1 m1 s1 " + role + "'>" +
				"<div class='mt30'><strong>" + role + "</strong></div>" + 
			"</div>" +
			"<div class='col l5 m5 s11 indigo lighten-5'>" +
				"<img class='imgcard' src='" + iconUrl + "'>" +
				"<img class='imgcard teamicon' src='" + teamUrl + "'><a class='waves-effect waves-light modal-trigger' onclick='openModal(\"" + name + "\",\"" + statsUrl + "\")'><strong>" + name + "</strong></a>" +
			"</div>" +
			"<div class='col l4 m3 s12 center'>" +
				getChip(myId, "Fg") + getChip(myId, "Gaz") + getChip(myId, "CdS") + getChip(myId, "Sky") +
			"</div>" +
			"<div id='" + name.toLowerCase() + "_match" + "' class='col l2 m3 s12 center'>" +
			"</div>" +
		"</div>";
	return chip;
}

function getChip(id, redazione) {
	var chipId = (id + "_" + redazione).toLowerCase();
	return "<div id='" + chipId + "' class='chip mt3 center'>" + redazione +"</div>";
}

function getTitolari() {
	var giornata = $( "#giornata" ).val();
	$.get( "gazzetta/matches/" + giornata, function( giornate ) {
		$( ".player" ).each(function( index ) {
			var team = $( this ).attr('team');
			var name = $( this ).attr('name');
			var match = giornate[team];
			$("#" + name + "_match").html(match['home'] + " - " + match['away']);
		});
	});
	
	$.get( "gazzetta/" + giornata, function( squadre ) {
		$( ".player" ).each(function( index ) {
			var team = $( this ).attr('team');
			var name = $( this ).attr('name');
			var titolari = squadre[team];
			if ($.inArray(name, titolari) !== -1 ) {
				$("#" + name + "_" + team + "_gaz").addClass('green');
			} else {
				$("#" + name + "_" + team + "_gaz").addClass('red');
			}
		});
		
	});
}

function loadTeam() {
	$("#titolari_btn").attr("disabled", true);
	$('#players').html("");
	if($( "#teamName" ).val() != "" && $( "#giornata" ).val() != "") {
		var team = $( "#teamName" ).val();
		var giornata = $( "#giornata" ).val();
		$.get( "get_team_players/" + team, function( data ) {
			team_players = data['players'];
			var ordered_players = orderPlayers(team_players);
			for (i = 0; i < ordered_players.length; i++) {
				var player = {};
				player['id'] = ordered_players[i]['id'];
				var chip = createTitolariChip(ordered_players[i]['id'], ordered_players[i]['role'], ordered_players[i]['iconUrl'], ordered_players[i]['name'], ordered_players[i]['statsUrl'], ordered_players[i]['teamUrl'], ordered_players[i]['team']);
		    	$("#players").append(chip);
			}
			$("#titolari_btn").removeAttr("disabled");
		});
	} else {
		Materialize.toast("Inserisci il nome squadra o la giornata", 3000);
	}
}

function deleteTeam() {
	if ($("#teamName").val()) {
		var team = $( "#teamName" ).val();
		$.ajax({
		    url: 'delete_team/' + team,
		    type: 'DELETE',
		    success: function(result) {
		    	Materialize.toast(result, 3000);
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
