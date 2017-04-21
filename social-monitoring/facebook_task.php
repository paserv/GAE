<?php 
use \Psr\Http\Message\ServerRequestInterface as Request;
use \Psr\Http\Message\ResponseInterface as Response;

require '/vendor/autoload.php';

$app = new \Slim\App;
$app->post('/stats', function (Request $request, Response $response) {
	$parent = $request->getParam('parent');
	$url = $request->getParam('url');
	$response->getBody()->write("Hello, $parent");
	
	return $response;
});
	$app->run();

?>