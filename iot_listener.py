#!/usr/bin/python3
#required libraries
import sys                                 
import json
import ssl
import subprocess
import paho.mqtt.client as mqtt
import time

#called while client tries to establish connection with the server 
def on_connect(mqttc, obj, flags, rc):
    print ('1a')

    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe([('$aws/things/<THING_NAME>/shadow/update/accepted',1) , ('$aws/things/<THING_NAME>/shadow/get/accepted',1)])

    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print ('1b')

    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))
    mqttc.publish('$aws/things/<THING_NAME>/shadow/get', payload='', qos=1, retain=False)

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print ('1c')
    #print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))

    payload=json.loads(msg.payload.decode())
    print(payload) 

    if 'desired' in payload['state']:
      print('L\n')
      desiredR=payload['state']['desired']['R']
      desiredG=payload['state']['desired']['G']
      desiredB=payload['state']['desired']['B']
      #print("desired:"+desiredUrl)
      
      reported = { "state": { "reported": {"R": str(desiredR),"G": str(desiredG),"B": str(desiredB) } } }
      reportMsg=json.dumps(reported)
      print("\nPlaying the following url: "+reportMsg)
      time.sleep(1) 
      
      mqttc.publish('$aws/things/<THING_NAME>/shadow/update', payload=reportMsg, qos=1, retain=False)  
     
    else:
      print('M\n')
      desiredR=payload['state']['desired']['R']
      desiredG=payload['state']['desired']['G']
      desiredB=payload['state']['desired']['B']
      print("\nreported:"+desiredR + desiredG + desiredB)
   
    
    reported = { "state": { "reported": {"R": str(desiredR),"G": str(desiredG),"B": str(desiredB) } } }
    reportMsg=json.dumps(reported)

    counter=1
    print("here") 

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="client3")
print ('1')

mqttc.on_connect = on_connect
print ('1')

mqttc.on_subscribe = on_subscribe
print ('1')

mqttc.on_message = on_message
print ('1')

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set("./certs/rootCA.pem",

            certfile="./certs/cert.pem",

            keyfile="./certs/private.pem",

              tls_version=ssl.PROTOCOL_TLSv1_2, 

              ciphers=None)
print ('2')

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("<END-POINT>.iot.us-east-1.amazonaws.com", port=8883) #AWS IoT service hostname and portno

print ('3')

#the topic to publish to
#automatically handles reconnecting

mqttc.loop_forever()
