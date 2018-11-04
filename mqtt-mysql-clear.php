#!/usr/bin/php
<?php

/************************************************************************
mqtt-mysql-clear.php
  - deletes ALL events from database

Copyright © 2015 Theo Arends
Modified 2018 by glitterkitty

************************************************************************/



// ==== MQTT MySQL parameters
$db_hostname = "localhost";		// MQTT MySQL server;
$db_database = "mqtt_data";
$db_username = "mqtt_user";
$db_password = "uwannaknowheh?";





echo "deleting ALL events from database $db_database on $db_hostname\n";



echo "connecting to db: $db_database on $db_hostname as $db_username\n";
$db = mysqli_connect($db_hostname, $db_username, $db_password, $db_database) or trigger_error(mysqli_error($db),E_USER_ERROR);




$query = "TRUNCATE TABLE messages";
echo "executing:  $query\n";
$result = mysqli_query($db, $query) or die(mysqli_error($db));


$query = "OPTIMIZE TABLE messages";
echo "executing:  $query\n";
$result = mysqli_query($db, $query) or die(mysqli_error($db));


echo "closing db\n";
mysqli_close($db);

echo "done.\n";

?>
