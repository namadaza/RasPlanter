var http = require('http');

var server = http.createServer(function(req, res) {
	res.writeHead(200);
	res.end('Hellow Http');
});
server.listen(8080);