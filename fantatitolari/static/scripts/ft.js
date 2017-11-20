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
			    	var chip = "<div class='row player' id='" + player['id'] +"'>" +
									"<div class='col offset-s1 " + playerRole + "'>" +
										"<div class='mt30'><strong>" + playerRole + "</strong></div>" + 
									"</div>" +
									"<div class='col s6 indigo lighten-5'>" +
										"<img class='imgcard' src='" + playermImgURL + "'><a class='waves-effect waves-light modal-trigger' href='#modalStats'><strong>" + playerName + "</strong></a>" +
									"</div>" +
									"<div class='col s2 indigo lighten-5'>" +
										"<img class='imgcard' src='" + teamImgURL + "'>" +
									"</div>" +
									"<div class='col indigo lighten-5'>" +
										"<i class='imgcard material-icons curpoint right' onclick='remove_player(" +  JSON.stringify(player) + ")'>close</i>" +
								"</div>" +
								"</div>";
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
			team_players = data['players'];
			$.each(team_players, function( index, value ) {
				var player = {};
				player['id'] = value['id'];
		    	$("#modalFrame").html("<iframe src='" + value['statsUrl'] + "' class='modalStats'></iframe>");
		    	$("#playerName").html("Statistiche " + value['name']);
		    	var chip = "<div class='row player' id='" + value['id'] +"'>" +
								"<div class='col offset-s1 " + value['role'] + "'>" +
									"<div class='mt30'><strong>" + value['role'] + "</strong></div>" + 
								"</div>" +
								"<div class='col s6 indigo lighten-5'>" +
									"<img class='imgcard' src='" + value['iconUrl'] + "'><a class='waves-effect waves-light modal-trigger' href='#modalStats'><strong>" + value['name'] + "</strong></a>" +
								"</div>" +
								"<div class='col s2 indigo lighten-5'>" +
									"<img class='imgcard' src='" + value['teamUrl'] + "'>" +
								"</div>" +
								"<div class='col indigo lighten-5'>" +
									"<i class='imgcard material-icons curpoint right' onclick='remove_player(" +  JSON.stringify(player) + ")'>close</i>" +
							"</div>" +
							"</div>";
		    	$("#players").append(chip);
				});
		});
		$("#delete_btn").removeAttr("disabled");
		$("#edit_btn").removeAttr("disabled");
	} else {
		$("#delete_btn").attr("disabled", true);;
		$("#edit_btn").attr("disabled", true);;
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

function clearInput() {
	$("#search").val(""); 
}
