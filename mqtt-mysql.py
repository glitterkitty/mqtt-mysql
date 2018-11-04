#!/usr/bin/python
#
# mqtt-mysql by Theo Arends
# Modified 2018 by glitterkitty
#
# Provides MQTT MySql service
#
# Execute: mqtt-mysql.py &
#
# Needs paho.mqtt.client
#   - git clone http://git.eclipse.org/gitroot/paho/org.eclipse.paho.mqtt.python.git
#   - python setup.py install
# Needs python MySql support
#   - apt-get install python-mysqldb
#
# <sub_prefix>/select
#   return all logged topics as JSON data
# <sub_prefix>/select/<topic>[%] [<minutes ago>|latest]
#   return logged topic data as JSON
# <sub_prefix>/setting/unique [0|1]
#   set or return a setting
#
# **** Start of user configuration values

broker      = "my_broker"   # MQTT broker ip address or name
broker_port = 1883          # MQTT broker port

sub_prefix = "solar/#"   # Own subscribe topic
pub_prefix = ""          # General publish topic, disabled when empty

db_hostname = "db_host"          # MySQL host ip address or name
db_database = "mqtt_data"       # MySQL database name
db_username = "mqtt_user"  # MySQL database user name
db_password = "uwannaknowheh?"   # MySQL database password


# **** End of user configuration values

M_VERSION = "1.1"
M_LOGLEVEL = 0                 # Print messages: 0 - none, 1 - Startup, 2 - MQTT and MySQL, 3 - All


import paho.mqtt.client as mqtt
import MySQLdb as mdb
import time
import datetime


def my_info(type, message):
  if type <= M_LOGLEVEL:
    print(message)



def log_message(msg):
  with con:
    cur = con.cursor()
    cur.execute("INSERT INTO messages (topic , qos, message) VALUES (%s, %s, %s)", (msg.topic, msg.qos, msg.payload))
    my_info(2, "MySQL INSERT INTO messages (topic_id , qos, message_id) VALUES ("+str(msg.topic)+", "+str(msg.qos)+", "+str(msg.payload)+")")



def get_setting(setting, default):
  state = default
  with con:
    cur = con.cursor()
    cur.execute("SELECT state FROM settings WHERE setting = %s", (setting))
    if cur.rowcount == 1:
      row = cur.fetchone()
      state = row[0]
    else:
      cur.execute("INSERT INTO settings (setting, state) VALUES (%s, %s)", (setting, default))
  return int(state)




def update_setting(setting, state):
  with con:
    cur = con.cursor()
    cur.execute("UPDATE settings SET state = %s WHERE setting = %s", (state, setting))
  return int(state)




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    
    my_info(1, "MQTT-MySql service connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    
    ## why do i connect to EVRYTHING? 
    ##client.subscribe([("#",0),("/#",0),("$SYS/broker/log/#",0)])

    client.subscribe( sub_prefix,0)




# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):


  my_info(2, "MQTT subscribed |"+msg.topic+"|"+str(msg.qos)+"|"+str(msg.payload)+"|")
  part = msg.topic.split("/",2)  # mysql/select/%
  if part[0] == sub_prefix:
    if len(part) > 1 and part[1] != "result":
      feedback = 1

      if part[1] == "version":
        mytopic = "version"
        payload = M_VERSION

      elif part[1] == "select":
        if len(part) > 2:
          topic = part[2]
          with con:
            cur = con.cursor()
            unique = 1
            try:
              history = int(msg.payload) * 60
              timestamp = datetime.datetime.fromtimestamp(time.time()-history).strftime('%Y-%m-%d %H:%M:%S')
              cur.execute("SELECT DISTINCT topic FROM messages \
                WHERE topic LIKE %s AND timestamp > %s", (topic+"%", timestamp))
              unique = cur.rowcount
              cur.execute("SELECT timestamp, topic, message FROM messages \
                WHERE topic LIKE %s AND timestamp > %s ORDER BY timestamp ASC LIMIT 1000", (topic+"%", timestamp))
            except:
              cur.execute("SELECT timestamp, topic, message FROM messages \
                WHERE topic LIKE %s ORDER BY timestamp DESC LIMIT 1", (topic+"%"))
              pass
            if cur.rowcount > 0:
              rows = cur.fetchall()
              payload = "["
              jsonnext = ""
              for row in rows:
                payload = payload + jsonnext + '{"time":"' + str(row[0]) +'"'
                if unique == 1 and S_UNIQUE != 0:
                  topic = str(row[1])
                else:
                  payload = payload + ',"topic":"' + str(row[1]) + '"'
                payload = payload + ',"value":"' + str(row[2]) + '"}'
                jsonnext = ","
              payload = payload + "]"
            else:
              payload = "none"
          mytopic = topic
        else:
          with con:
            cur = con.cursor()
            cur.execute("SELECT DISTINCT topic FROM messages ORDER BY topic ASC LIMIT 1000")
            if cur.rowcount > 0:
              rows = cur.fetchall()
              payload = "["
              jsonnext = ""
              for row in rows:
                payload = payload + jsonnext + '{"topic":"' + str(row[0]) + '"}'
                jsonnext = ","
              payload = payload + "]"
            else:
              payload = "none"
          mytopic = "topics"

      elif part[1] == "setting":
        feedback = 0
        if len(part) > 2:
          mytopic = part[2]
          myset = mytopic.split("/",2)

          if len(msg.payload) > 0:  # Set
            state = "0"
            if str(msg.payload)[0] != "0":
              state = "1"
            if myset[0] == "unique":
              S_UNIQUE = update_setting(myset[0], state)

          else:     # Get
            if myset[0] == "unique":
              payload = str(get_setting(myset[0], F_UNIQUE))
              feedback = 1

      else:
        feedback = 0

      if feedback == 1:
        mytopic = sub_prefix + "/result/" + mytopic
        myquote = '"'
        if payload[0] == "[":
          myquote = ""
        payload = '{"result":' + myquote + payload + myquote +'}'
        my_info(2, "MQTT  published |"+mytopic+"|"+payload+"|")
        client.publish(mytopic, payload)

  else:
    log_message(msg)





my_info(1, "MQTT mysql service "+ M_VERSION)

mainloop = 1
while mainloop == 1:
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  dc = 1
  while dc == 1:
    try:
      con = mdb.connect(db_hostname, db_username, db_password, db_database)
      dc = 0
      my_info(1, "Database connected")
      
    except:
      my_info(1, "Warning: No database (connection) found. Retry in one minute.")
      time.sleep(60)
      pass


  rc = 1
  while rc == 1:
    try:
      client.connect(broker, broker_port)
      rc = 0
      my_info(1, "MQTT-Broker connected")
      
    except:
      my_info(1, "Warning: No broker found. Retry in one minute.")
      time.sleep(60)
      pass



  if pub_prefix:
    my_info(1, "Publishing on "+pub_prefix)
    client.publish(pub_prefix+"/MySql/MESSAGE", "Connection with broker established.")



  while rc == 0:
    try:
      rc = client.loop()
    except:
      rc = 1



  print("Warning: Connection error - Restarting.")



  # keep running when not debugging
  if M_LOGLEVEL > 0:
    mainloop = 0
