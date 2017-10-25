<?php 
use \Psr\Http\Message\ServerRequestInterface as Request;
use \Psr\Http\Message\ResponseInterface as Response;

require '/vendor/autoload.php';
require_once('TwitterAPIExchange.php');


$app = new \Slim\App;
$app->get('/stats', function (Request $request, Response $response) {
	$parent = $request->getParam('param');
	
	$settings = array(
		'oauth_access_token' => "90233211-WaN872hBupVTThJJBP5zPsSNvMSiw1w29OXvKj273",
		'oauth_access_token_secret' => "TrRzTLc1fpVmKslZy0bUOGcAVFvn1xbLieLF3Z47vNqrG",
		'consumer_key' => "f1mboyRyl229y3cXCFkKBJrLP",
		'consumer_secret' => "dNXHcIzQGk07fEVxPvgUt3ZfPNmxi4MYOYsyokdOQcAavnIvb1"
	);
	
	$url = 'https://api.twitter.com/1.1/followers/ids.json';
	$getfield = '?screen_name=J7mbo';
	$requestMethod = 'GET';
	
	$twitter = new TwitterAPIExchange($settings);
	
	echo $twitter->setGetfield($getfield)->buildOauth($url, $requestMethod)->performRequest();	
	$response->getBody()->write('Hello', $parent );
	
	return $response;
});

$app->run();

?>