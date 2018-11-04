# mqtt-mysql
MQTT mysql client and server

Copyright © 2015 Theo Arends
Modified 2018 by glitterkitty


Motivation for this fork:
Having a (really) small solar setup with an epever ls1024b charge-controller conneted via modbus to a wemos-d1-mini publishing data to a mosquitto mqtt-broker on an odroid-c2 running ubuntu 16.04 sitting in a small wooden box I made myself using handtools only, I wanted what ev'rybody and his dog wants: to get the mqtt-data to my mariaDB database to be able to maybe use it later on in grafana and/or the like.

So, whe I stumbled upon the original repo, it didn't run at first, or didn't run the way I wanted, or was too unverbose for my liking, plus there was no information on how to use this. So I modified the code, wrote down this readme and setup a fork, in case someone else might wanna use this and got stuck with the original code.


Prerequisites:
- have a database-server at hand
- have an mqtt-broker running
- edit the scripts/files to reflect your settings (hosts,usernames,passes,etc.)
- init the database by running 'mysql < init_db.sql' (only tested with mariaDB) 


Usage:
- run 'python mqtt-mysql.py' to catch mqtt-messages and let them be stored to a database
- run 'php mqtt-mysql-clean.php' to remove all messages older than 30 days
- run 'php mqtt-mysql-clear.php' to remove ALL messages, regardless of age


Changes in this fork:

- added file-extensions for clarity  
- renamed/added files
- added some verboseness

php scripts:
  - split up into 2 script: one for 'housekeeping', one for 'burning down the house'
  - rewitten parts to reflect the transitions from mysql_* to mysqli_* in php

mqtt-mysql.py:
- rewritten mqtt-mysql to be more verbose when connecting
- rewritten mqtt-mysql to subscribe to a single topic only (you can use wildcards to catch subtopics)

init_db.sql:
- renamed file
- renamed db
- added commands to create user and grant access



Notes:

On my system I had to additionally install packages, modules, etc.:

    pip2 install paho-mqtt
    sudo apt-get install python-mysqldb
    (maybe more, it was a hassle...)
    
I have tested it only with flat mqtt-messages, not with json-data

    
    
The Grafana-Part:
  - yet untested - t.b.h.: I don't even know if this will work this way :)
   
 

Good Luck
    


    




