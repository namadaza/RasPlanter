var express = require('express'),
	app = express(),
	server = require('http').createServer(app),
	io = require('socket.io').listen(server);
	
server.listen(8080);

app.get('/', function(req, res) {
	res.sendfile(__dirname + '/2testJSonMidori.html');
});

//function called upon a client connecting to the server
io.sockets.on('connection', function(socket) {
	
	//socket acts upON receving the 'get_days' event from the client
	//parse the data recieved, adding the command type, print to console,
	//emit a success event back to clients
	socket.on('get_days', function(data) {
		//var parsedCommand = "setDays::"+data;
		//console.log("Days from client: "+parsedCommand);
		io.sockets.emit('days set', data);		
		//socket.broadcast.emit('days set', data);
	});
});