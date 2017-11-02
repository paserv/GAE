var anagraficaGiocatori = {}
function populate_players() {
	$.get( "get_players", function( players ) {
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

function saveTeam() {
	if ($("#teamName").val()) {
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
	} else {
		Materialize.toast("Inserisci il nome squadra", 3000);
	}

}

