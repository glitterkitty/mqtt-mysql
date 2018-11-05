# mqtt-mysql
MQTT mysql client and server

Copyright © 2015 Theo Arends<br>
Modified 2018 by glitterkitty


## Motivation for this fork:
Having a (really) small solar setup with an epever ls1024b charge-controller conneted via modbus to a wemos-d1-mini publishing data to a mosquitto mqtt-broker on an odroid-c2 running ubuntu 16.04 sitting in a small wooden box I made myself using handtools only, I wanted what ev'rybody and his dog wants: to get the mqtt-data to my mariaDB database to be able to maybe use it later on in grafana and/or the like.

So, when I stumbled upon the original repo, it didn't run at first, or didn't run the way I wanted, or was too unverbose for my liking, plus there was no information on how to use this. So I modified the code, wrote down this readme and setup a fork, in case someone else might wanna use this and got stuck with the original code.


## Prerequisites:
- have a database-server at hand
- have an mqtt-broker running
- edit the scripts/files to reflect your settings (hosts,usernames,passes,etc.)
- init the database by running 'mysql < init_db.sql' (only tested with mariaDB) 


## Usage:
- run 'python mqtt-mysql.py' to catch mqtt-messages and let them be stored to a database
- run 'php mqtt-mysql-clean.php' to remove all messages older than 30 days
- run 'php mqtt-mysql-clear.php' to remove ALL messages, regardless of age


## Changes in this fork:
- added file-extensions for clarity  
- renamed/added files
- added some verboseness

### php scripts:
  - split up into 2 script: one for 'housekeeping', one for 'burning down the house'
  - rewitten parts to reflect the transitions from mysql_* to mysqli_* in php

### mqtt-mysql.py:
- rewritten mqtt-mysql to be more verbose when connecting
- rewritten mqtt-mysql to subscribe to a single topic only (you can use wildcards to catch subtopics)

### init_db.sql:
- renamed file
- renamed db
- added commands to create user and grant access



## Notes:

### packages needed:
On my system I had to additionally install packages, modules, etc.:

    pip2 install paho-mqtt
    sudo apt-get install python-mysqldb
    (maybe more, it was a hassle...)
    
### testing:
I have tested it only with flat mqtt-messages, not with json-data.<br>

Setting M_LOGLEVEL = 2 in mqtt-mysql.py gives you useful information when using for the first time, e.g. if the database connection works, the mqtt broker can be connected and whether mqtt data is coming in or not. You can issue the following command on another terminal to produce test-data:

    mosquitto_pub -h <your_mqtt_broker> -t <your_mqtt_topic> -m test
    
    
## Running as a service:

After testing and copying all the files to `/srv/mqtt-mysql/` as user root, create a service-file with `sudo nano /etc/systemd/system/mqtt-mysl.service`:

```[Unit]
Description=mqtt-mysql service
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python /srv/mqtt-mysql/mqtt-mysql.py

[Install]
WantedBy=multi-user.target
```
Then
- enable service: `sudo systemctl enable mqtt-mysl`
- start service: `systemctl start mqtt-mysl`
- check service: `systemctl status mqtt-mysl` and `sudo journalctl -xe | grep mqtt-mysql`

Usign a database-viewer (adminer), you can checked the database for incoming data.


    
## The Grafana-Part:
  - ~~yet untested - t.b.h.: I don't even know if this will work this way :)~~
  - setup mysql as data-source
  - add a panel using that data-source for metrics
  - edit sql-query, e.g.:
  ```
    SELECT
    UNIX_TIMESTAMP(timestamp) as time_sec,
    convert(message,DOUBLE) as value,
    "Voltage Battery" as metric
    FROM messages
    WHERE topic="solar/battery/V"
    ORDER BY timestamp ASC 
```

  - setup axes, title, etc.
   
   
## Todo:
 - I think, the database scheme ain't that sophisticated and needs some reworking
 - more to come...
 
## 
Good Luck
    


    




