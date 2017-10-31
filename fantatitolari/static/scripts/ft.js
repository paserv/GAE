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
		    	if ($("[id='" + val + "']").length) {
		    		Materialize.toast("Giocatore presente", 3000);
		    	} else {
		    		var playerName = val.split('(')[0].trim();
		    		var playermImgURL = anagraficaGiocatori[playerName]['iconUrl'];//"https://content.fantagazzetta.com/web/campioncini/small/" + playerName.replace(" ", "-") + ".png";
		    		var teamImgURL = anagraficaGiocatori[playerName]['teamUrl'];
		    		var statsUrl = anagraficaGiocatori[playerName]['statsUrl'];
		    		var playerRole = anagraficaGiocatori[playerName]['role'];//val.split('(')[1][0];
		    		var player = {};
			    	player['id'] = anagraficaGiocatori[playerName]['id'];//val;
			    	var chip = "<div class='row' id='" + player['id'] +"'>" +
									"<div class='col offset-s1 " + playerRole + "'>" +
										"<div class='mt30'><strong>" + playerRole + "</strong></div>" + 
									"</div>" +
									"<div class='col s4 indigo lighten-5'>" +
										"<img class='imgcard' src='" + playermImgURL + "'><a href='" + statsUrl  + "'><strong>" + playerName + "</strong></a>" +
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

