/*
 * © 2016 - Julián Acosta
 * License: CC BY-SA 4.0 (http://creativecommons.org/licenses/by-sa/4.0/)
 * 
 * Print your own logo in developer tools!
 *
 * Step 1: Convert your logo to ASCII text here: http://picascii.com (I used color output)
 *      Note: Is possible that you'll have to resize your photo in order to retain aspect ratio
 * Step 2: Remove the <pre></pre> tag that is surrounding the generated code, replace with "[" and "]"
 * Step 3: Run the following regexes (*DON'T ALTER THE ORDER*) in order to convert to JSON (Works in PHPStorm and Sublime Text 2):
 *      3a: Find: '<\/span>' (without quotes)
 *          Replace: '<\/span>\n'
 *      3b: Find: '<span style=\"(.*?)\"[^>]*>(.*?)<\/span>' (without quotes)
 *          Replace: '{ \"text\": \"$2\", \"style\": \"$1\ background-color: #FFF\"};'
 *      3c: Find: '<span style=\"(.*?)\"[^>]*>(.*?)\n<\/span>' (without quotes)
 *          Replace: 'params.push("background-color: #FFF; $1"); message+="%c$2\\n";' //(Note the escaped backslash)
 *      3d: Find: '\},(\n| |\t)\]' (without quotes)
 *          Replace: '\}\n\]'
 *      Note: background-color is used in firefox (background in console is light-gray)
 * Step 4: Save your JSON file
 *
 * Voila!
 *
 * W̶A̶R̶N̶I̶N̶G̶:̶ ̶V̶e̶r̶y̶ ̶b̶i̶g̶ ̶i̶m̶a̶g̶e̶s̶ ̶w̶i̶l̶l̶ ̶s̶l̶o̶w̶ ̶d̶o̶w̶n̶ ̶y̶o̶u̶r̶ ̶s̶i̶t̶e̶,̶ ̶b̶e̶c̶a̶u̶s̶e̶̶c̶o̶n̶s̶o̶l̶e̶ ̶i̶s̶ ̶n̶o̶t̶ ̶o̶p̶t̶i̶m̶i̶z̶e̶d̶ ̶t̶o̶ ̶d̶o̶ ̶t̶h̶i̶s̶,̶
 * s̶o̶ ̶t̶a̶k̶e̶ ̶t̶h̶i̶s̶ ̶i̶n̶ ̶m̶i̶n̶d̶ ̶w̶h̶e̶n̶ ̶y̶o̶u̶ ̶a̶r̶e̶ ̶u̶s̶i̶n̶g̶ ̶t̶h̶i̶s̶ ̶i̶n̶ ̶p̶r̶o̶d̶u̶c̶t̶i̶o̶n̶. It seems fixed by using JSON instead of
 * hardcoding parameters in JS file.
 *
 */

//Params that will be passed to console.log function
var params = [];

//String that will contain all the logo characters
var message = "";

//Request to our JSON file
var request = new XMLHttpRequest ();
request.overrideMimeType ("application/json");
request.open ('GET', 'static/logo.ascii', true); //Replace with URL to your JSON file

//Executed when request was made
request.onreadystatechange = function onJSONFileRead () {

	//If request is sucessful
	if (request.readyState == 4 && request.status == "200") {

		//Parsing JSON file
		var json = JSON.parse (request.responseText);

		//Adding JSON entries to params array
		for (var i = 0; i < json.length; i++) {
			message += '%c' + json [i].text;
			params.push (json [i].style);
		}

		//Adding string to first position of array
		params.unshift (message);

		//Using apply to pass params as array
		console.log.apply (console, params);

	}
};

request.send ();