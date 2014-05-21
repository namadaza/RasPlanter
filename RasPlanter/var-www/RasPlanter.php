<html>

<head>
	<title>RasPlanter</title>
	<link rel="stylesheet" type="text/css" href="RasPlanterStyle.css"></link
</head>

<script src="http://code.jquery.com/jquery.min.js"></script>
<script type="text/javascript" language="javascript" src="jquery.flot.js"></script>
<script>
$(document).ready(function() {
	  //draw graphs for incoming values from server
	  var totalPoints = 600;
	  var lumenVals = [];
	  var tempVals = [];
	  var humidVals = [];
	  
	  var lumenPlot = $.plot("#lumensGraphID", [lumenVals], {
			series: {
				shadowSize: 0	// Drawing is faster without shadows
			},
			yaxis: {
				min: 0,
				max: 1500
			},
			xaxis: {
				min: 0,
				max: 60,
				show: true
			}
		});

	   var tempPlot = $.plot("#tempGraphID", [tempVals], {
			series: {
				shadowSize: 0	// Drawing is faster without shadows
			},
			yaxis: {
				min: 25,
				max: 100
			},
			xaxis: {
				min: 0,
				max: 60,
				show: false
			}
		});

	    var humidPlot = $.plot("#humidGraphID", [humidVals], {
			series: {
				shadowSize: 0	// Drawing is faster without shadows
			},
			yaxis: {
				min: 0,
				max: 1000
			},
			xaxis: {
				min: 0,
				max: 60,
				show: false
			}
		});

	  
       //The user has WebSockets
      $("#experimentRunning").hide();
      $("#standingBy").hide();
      
      connect();
      function connect(){
      	  
          var socket;
          var host = "ws://192.168.1.20:8000/ws";
          var status=setInterval(function() {checkStatus()}, 5000);
          var screenLoaded="0";
          var getReturns=0;
 			
          try{
              var socket = new WebSocket(host);
  
              socket.onopen = function(){
                 //message('<p class="event">Socket Status: '+socket.readyState+' (open)');
              	 $("#connected").hide();
              	 $("#standingBy").show();
              	 startTime = new Date();
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
                 else if (parsedData[0]=="testOn") {
                 	if(parsedData[1]=="1") {
                 		if (screenLoaded=="0") {
                 			loadScreen();
                 		}
                 	}
                 	else if(parsedData[1]=="0") {
                 		standByScreen();
                 	}
                 }
              }
 
              socket.onclose = function(){
                //message('<p class="event">Socket Status: '+socket.readyState+' (Closed)');
              }         
 
          } 
          catch(exception){
             //message('<p>Error'+exception);
          }
          
          var totalPoints = 70;
          var data1 = [];
          var data2 = [];
          var data3 = [];
			
		  var lumdata = 0;

		  function getLumenData() {
		  	if ($("#getLumens").val()=="") {
		  		lumdata=0;
		  	}
		  	else {
		  		lumdata = $("#getLumens").val();
		  		
		  	}
			if (data1.length > 0)
				data1 = data1.slice(1);

			// Do a random walk
			while (data1.length < totalPoints) {
				var prev = data1.length > 0 ? data1[data1.length - 1] : 50,
					y = $("#getLumens").val()

				if (y < 0) {
					y = 0;
				} else if (y > 1500) {
					y = 1500;
				}
				data1.push(y);
			}
			// Zip the generated y values with the x values
			var res = [];
			for (var i = 0; i < data1.length; ++i) {
				res.push([i, data1[i]])
			}
			return res;
		  }
		  
		  function getTempData() {
		  	if ($("#getTemperature").val()=="") {
		  		tempdata=0;
		  	}
		  	else {
		  		tempdata= $("#getTemperature").val();
		  		
		  	}
			if (data2.length > 0)
				data2 = data2.slice(1);

			// Do a random walk
			while (data2.length < totalPoints) {
				var prev = data2.length > 0 ? data2[data2.length - 1] : 50,
					y = $("#getTemperature").val()

				if (y < 0) {
					y = 0;
				} else if (y > 1500) {
					y = 1500;
				}
				data2.push(y);
			}
			// Zip the generated y values with the x values
			var res = [];
			for (var i = 0; i < data2.length; ++i) {
				res.push([i, data2[i]])
			}
			return res;
		  }

		function getHumidData() {
		  	if ($("#getHumidity").val()=="") {
		  		humiddata=0;
		  	}
		  	else {
		  		humiddata= $("#getHumidity").val();
		  		
		  	}
			if (data3.length > 0)
				data3 = data3.slice(1);

			// Do a random walk
			while (data3.length < totalPoints) {
				var prev = data3.length > 0 ? data3[data3.length - 1] : 50,
					y = $("#getHumidity").val()

				if (y < 0) {
					y = 0;
				} else if (y > 1000) {
					y = 1000;
				}
				data3.push(y);
			}
			// Zip the generated y values with the x values
			var res = [];
			for (var i = 0; i < data3.length; ++i) {
				res.push([i, data3[i]])
			}
			return res;
		  }


		  var updateInterval = 1000;
		  function update() {

			lumenPlot.setData([getLumenData()]);
			tempPlot.setData([getTempData()]);
			humidPlot.setData([getHumidData()]);

			// Since the axes don't change, we don't need to call plot.setupGrid()

			lumenPlot.draw();
			tempPlot.draw();
			humidPlot.draw();
			setTimeout(update, updateInterval);
		  }
  
		  update();

  	
          //assign zeroes to command identifies as not need, only for 
          //python splitting	
          //run every three seconds while test is running
          //repeatedly send get commands every 3 seconds
          //to refresh returned data from RasPlanter
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
          
          function checkStatus() {
          		var isTestOnCommand = "isTestOn::0";     		
          		socket.send(isTestOnCommand);
          };
          
          function loadScreen() {
          		getReturns=setInterval(function() {getReturnedVals()},3000);
          		$("#standingBy").hide();
          		$("#experimentRunning").show();
          		screenLoaded="1";
		  };
		  
		  function standByScreen() {
				$("#standingBy").show();
          		$("#experimentRunning").hide();
				clearInterval(getReturns);
				screenLoaded="0";
		  };

 
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
          	var startTestCommand = "startTest::"+1;
           	       
          	socket.send(setDaysCommand);
          	socket.send(setLightcycleCommand);
          	socket.send(setLumensCommand);
          	socket.send(setTempCommand);
         	socket.send(setHumidityCommand);
         	socket.send(startTestCommand);    
         	
			loadScreen();       	
          });
          
          
          $("#stopTest").click(function(evt) {
          	//end test functions
          	evt.preventDefault();
          	var stopTestCommand = "stopTest::0";
          	socket.send(stopTestCommand);
          	
          	//clear interval set last to hold off further gets from client
          	standByScreen();
          });

      }//End connect  	
});
</script>
<body>

<h1>RasPlanter</h1>
<div class="status">
	<div id="experimentRunning">
		<h3 style="width: 343px; height: 22px">EXPERIMENT RUNNING</h3>
	</div>
	<div id="standingBy">
		<h3 style="width: 343px; height: 19px">STANDING BY</h3>
	</div>
	<div id="connected">
		<h3 style="width: 343px;height: 22px">WAITING FOR CONNECTION</h3>
	</div>
</div>

<div class="variablesField">
	<h2>Values from RasPlanter</h2>
	<form method="post" div="setVariablesField">
		<div class="graphs">
			<p>Lumens:</p>
				&nbsp;<input id="getLumens" type="text">	
			<div id="lumensGraphID"></div>
			
			<p>Temperature:</p>
				&nbsp;<input id="getTemperature" type="text">
			<div id="tempGraphID"></div>
			
			<p>Humidity:</p>
				&nbsp;<input id="getHumidity" type="text">
			<div id="humidGraphID"></div>
		</div>
		
		<p>Days set:</p>
			&nbsp;<input id="getDays" type="text">
		<p>Lightcycle set:</p>
			&nbsp;<input id="getLightcycle" type="text">
		<p>Stop Test?</p>
			&nbsp;<input id="stopTest" type="submit" value="Yes">
	</form>
</div>

<div class="setVariables">
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
</div>

</body>
</html>
