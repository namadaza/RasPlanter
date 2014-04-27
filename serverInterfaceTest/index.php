<html><body><h1>RasPlanter</h1>
<p>Set Variables</p>

<p>Number of Days to run test:</p>
<form method="post" action="index.php">
	<input type="text" name="days">
	<input type="submit" value="submit" name="submit">
</form>

<p>Length of Light Cycle in Hours:</p>
<form method="post" action="index.php">
	<input type="text" name="time_of_lightcycle">
	<input type="submit" value="submit" name="submit1">
</form>

<p>Desired Lumens:</p>
<form method="post" action="index.php">
	<input type="text" name="lumens">
	<input type="submit" value="submit" name="submit2">
</form>

<p>Desired Temperature:</p>
<form method="post" action="index.php">
	<input type="text" name="temperature">
	<input type="submit" value="submit" name="submit3">
</form>

<p>Desired Soil Humidity:</p>
<form method="post" action="index.php">
	<input type="text" name="humidity">
	<input type="submit" value="submit" name="submit4">
</form>

<p>Start Test:</p>
<form method="post" action="index.php">
	<input type="radio" name="start_test" value="1">True<br>
	<input type="radio" name="start_test" value="0">False<br>
	<input type="submit" value="submit" name="submit5">
</form>

<?php
	ini_set('display_errors', 'On');
	error_reporting(E_ALL);
	
	function display() {
		echo "Days: ".$_POST["days"];
		echo "Lightcycle: ".$_POST["time_of_lightcycle"];
		echo "Lumens: ".$_POST["lumens"];
		echo "Temperature: ".$_POST["temperature"];
		echo "Soil Humidity: ".$_POST["humidity"];
	}
	
	if(!empty($_POST)) {
		$host = "127.0.0.1";
		$port = 5555;
		//echo "Desired Variable".$message;
		if (isset($_POST["days"])) {
			$message = "setDays::" . $_POST["days"];
		}
		elseif (isset($_POST["time_of_lightcycle"])) {
			$message = "setLightcycle::" . $_POST["time_of_lightcycle"];
		}
		elseif(isset($_POST["lumens"])) {
			$message = "setLumens::" . $_POST["lumens"];
		}
		elseif (isset($_POST["temperature"])) {
			$message = "setTemperature::" . $_POST["temperature"];
		}
		elseif (isset($_POST["humidity"])){
			$message = "setHumidity::" . $_POST["humidity"];
		}
		elseif (isset($_POST["start_test"])) {
			$message = "startTest::" . $_POST["start_test"];
		}
		//create socket
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP) or
					 die("could not create socket\n");
		//conect to server
		$result = socket_connect($socket, $host, $port) or
					die("could not connect socket\n");
		//get server resposnse
		//$result = socket_read($socket, 1024) or
		//			die("could not read server response\n");
		//echo "Replay From Server: ".$result;
		//close socket
		//send string to server
		socket_write($socket, $message, strlen($message)) or
					die("could not send data to server\n");
		socket_close($socket);
	}
?>

</body></html>
