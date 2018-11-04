

CREATE DATABASE mqtt_data;
USE mqtt_data;

DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
  timestamp   timestamp DEFAULT CURRENT_TIMESTAMP,
  topic       text NOT NULL,
  qos         tinyint(1) NOT NULL,
  message     text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS settings;
CREATE TABLE settings (
  setting     varchar(8) NOT NULL PRIMARY KEY,
  state       tinyint(1) NOT NULL,
  timestamp   timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARSET=utf8;


CREATE USER mqtt_user@localhost IDENTIFIED BY 'password';
GRANT ALL privileges ON mqtt_data.* TO mqtt_user ;

