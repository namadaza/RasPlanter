<html>

<head>
<style type="text/css">
.auto-style1 {
	margin-top: 19px;
}
</style>
</head>

<script src="http://code.jquery.com/jquery.min.js"></script>
<script>
$(document).ready(function() {
       //The user has WebSockets
      connect();
      function connect(){
          var socket;
          var host = "ws://192.168.1.28:8080/ws";
 
          try{
              var socket = new WebSocket(host);
  
              socket.onopen = function(){
                 //message('<p class="event">Socket Status: '+socket.readyState+' (open)');
              }
 
              socket.onmessage = function(msg){
              	 //data from server recieved HERE
                 //message('<p class="message">Received: '+msg.data);
                 //parse incoming data, funnel data to appropriate text fields
                 var unparsedData = msg.data;
                 var parsedData = unparsedData.split('::');
                 
                 if (parsedData[0]=="returnedDays") {
                 	$('#getDays').removeAttr('readonly').val(parsedData[1]);
                 }
                 else if (parsedData[0]=="returnedLightcycle") {
                 	$("#getLightcycle").removeAttr('readonly').val(parsedData[1]);
                 }
                 else if (parsedData[0]=="returnedLumens") {
                 	$("#getLumens").removeAttr('readonly').val(parsedData[1]);
                 }
				 else if (parsedData[0]=="returnedTemp") {
                 	$("#getTemperature").removeAttr('readonly').val(parsedData[1]);
                 }
                 else if (parsedData[0]=="returnedHumidity") {
                 	$("#getHumidity").removeAttr('readonly').val(parsedData[1]);
                 }
              }
 
              socket.onclose = function(){
                //message('<p class="event">Socket Status: '+socket.readyState+' (Closed)');
              }         
 
          } 
          catch(exception){
             //message('<p>Error'+exception);
          }
 
          $('#startTest').click(function(evt){
            //on clicking startTestTrue button,
            //set values from text fields inputted by user
            //add data identifier to data
            //send as individual commands to RasPlanter.py
          	evt.preventDefault();
          	var days = $("#days").val();          
          	var lightcycle = $("#time_of_lightcycle").val();
          	var lumens = $("#lumens").val();
          	var temp = $("#temperature").val();
          	var humidity = $("#humidity").val();
          	
          	var setDaysCommand = "setDays::"+days;
          	var setLightcycleCommand = "setLightcycle::"+lightcycle;
          	var setLumensCommand = "setLumens::"+lumens;
          	var setTempCommand = "setTemperature::"+temp;  
          	var setHumidityCommand = "setHumidity::"+humidity;
          	var startTest = "startTest::"+1;
           	       
          	socket.send(setDaysCommand);
          	socket.send(setLightcycleCommand);
          	socket.send(setLumensCommand);
          	socket.send(setTempCommand);
         	socket.send(setHumidityCommand);
         	socket.send(startTest);
         	
         	//assign zeroes to command identifies as not need, only for 
         	//python splitting
         	function getReturnedVals() {
          		var getDaysCommand = "getDays::0";
          		var getLightcycleCommand = "getLightcycle::0";
          		var getLumensCommand = "getLumens::0";
          		var getTempCommand = "getTemp::0";
          		var getHumidityCommand = "getHumidity::0";
          	
          		socket.send(getDaysCommand);
          		socket.send(getLightcycleCommand);
          		socket.send(getLumensCommand);
          		socket.send(getTempCommand);
          		socket.send(getHumidityCommand);
         	};
          	
          	//run every three seconds while test is running
          	var getReturns=setInterval(function() {getReturnedVals()},3000);
          });
          
          //repeatedly send get commands every 3 seconds
          //to refresh returned data from RasPlanter
          
          $("#stopTest").click(function(evnt) {
          	//end test functions
          });

      }//End connect  	
});
</script>
<body>
<h1>RasPlanter</h1>

<h2>Set Variables</h2>
<p>Number of Days to run test:</p>
<form method="post" action="index.php">
	<input type="text" id="days">&nbsp;
</form>

<p>Length of Light Cycle in Hours:</p>
<form method="post" action="index.php">
	<input type="text" id="time_of_lightcycle">&nbsp;
</form>

<p>Desired Lumens:</p>
<form method="post" action="index.php">
	<input type="text" id="lumens">&nbsp;
</form>

<p>Desired Temperature:</p>
<form method="post" action="index.php">
	<input type="text" id="temperature">&nbsp;
</form>

<p>Desired Soil Humidity:</p>
<form method="post" action="index.php">
	<input type="text" id="humidity">&nbsp;
</form>

<p>Start Test:</p>
<form method="post">
	<input id="startTest" type="submit" value="Yes"><input name="startTestFalse" type="reset" value="No"></form>


<h2>Values from RasPlanter</h2>
<form method="post" div="setVariablesField">
	<p>Days set:</p>
	&nbsp;<input id="getDays" type="text">
	<p>Lightcycle set:</p>
	&nbsp;<input id="getLightcycle" type="text">
	<p>Lumens:</p>
	&nbsp;<input id="getLumens" type="text">
	<p>Temperature:</p>
	&nbsp;<input id="getTemperature" type="text">
	<p>Humidity:</p>
	&nbsp;<input id="getHumidity" type="text">
	<p>Stop Test?</p>
	&nbsp;<input id="stopTest" type="submit" value="Yes">
</form>

</body>
</html>
