function populate_players() {
	$.get( "get_players", function( players ) {
		$('input.autocomplete').autocomplete({
		    data: players,
		    limit: 20, // The max amount of results that can be shown at once. Default: Infinity.
		    onAutocomplete: function(val) {
		    	if ($("[id='" + val + "']").length) {
		    		Materialize.toast("Giocatore presente", 3000);
		    	} else {
		    		var player = {};
			    	player['id'] = val;
			    	$("#players").append("<div id='" + val + "'>" + val + "<i class='material-icons curpoint' onclick='remove_player(" +  JSON.stringify(player) + ")'>close</i></div>");
		    		}
		    	},
		    minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
		  });
	});
}

function remove_player(player) {
	$("[id='" + player['id'] + "']").remove();
}

