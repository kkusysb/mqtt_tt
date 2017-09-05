import paho.mqtt.client as mqtt
import json
import configparser


# Define Variables
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "tele/sonoff/SENSOR"

DOMOTICZ_IN_TOPIC = "domoticz/in"

d_idx=[0,0,0,0,0,0,0,0]
#d_map={'DS1':0 ,'DS2':0,'DS3':0,'DS4':0}
d_map={
"28E067BF08000059" : 2 ,
"28CC70BF080000BF": 3 ,
"282E24BD08000075": 4 ,
"28AD24BE0800004E": 5 ,
"28FFA626A216055E": 6 }

MQTT_MSG={"idx": 0 ,"nvalue":  0 ,"svalue": "0"};


# Define on_publish event function
def on_publish(client, userdata, mid):
    print( "Message Published...")

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
    #client.publish(MQTT_TOPIC, MQTT_MSG)

def on_message(client, userdata, msg):
    print("onmessage:")
    print("topic=" + msg.topic)
    print("payload=",)
    #try:
    print(msg.payload) 
    payload = json.loads(msg.payload) 
    print(payload)
    #try :
        #s=payload['DS18x20']['DS1']
        #print(s)
    try:
        for n in range(1,8):
            s='DS'+str(n)
            print('s=',s)
            s=payload['DS18x20'][s]
            print('s=',s)
            sv=s['Temperature']
            ad=s['Address']
            print('ds=',ad,' ',sv)
            MQTT_MSG['svalue']=str(sv)
            i=d_map[ad]
            MQTT_MSG['idx']=i
            print(MQTT_MSG)
            out =json.dumps(MQTT_MSG)
            print('py=', out)
            client.publish(DOMOTICZ_IN_TOPIC, out)

        #for i in d_map:
        #  print(i)
        #  if d_map[i] > 0 :  
        #    s=payload['DS18x20'][i]
        #    print(s)
        #    sv=s['Temperature']
        #    print(sv)
        #    MQTT_MSG['svalue']=str(sv)
        #    MQTT_MSG['idx']=d_map[i]
        #    print(MQTT_MSG)
        #    out =json.dumps(MQTT_MSG)
        #    print('py=', out)
        #    client.publish(DOMOTICZ_IN_TOPIC, out)
    except: 
        #pass
        print ("exc")

    #for i==
    #MQTT_MSG['idx']= d_idx[i]
    #print(MQTT_MSG)



MQTT_TOPICS= []
d_map={}

cfg = configparser.ConfigParser(allow_no_value=True)
cfg.optionxform = str
cfg.read('mqtt_tr.cfg')
print ('cfg=',cfg)


if 'mqtt_topics' in cfg:
    for key in cfg['mqtt_topics']:
        print('key',key)
        MQTT_TOPICS.append(key)
print('MQTT_TOPICS=',MQTT_TOPICS)

if 'map_devices' in cfg:
    for key in cfg['map_devices']:
        print('key',key)
        idx= cfg['map_devices'][key]    
        print('idx',idx)
        d_map[key]=int(idx)
print('d_map',d_map)

MQTT_HOST= cfg['app'].get('MQTT_HOST',MQTT_HOST)
MQTT_PORT= int( cfg['app'].get('MQTT_PORT',MQTT_PORT) )
MQTT_KEEPALIVE_INTERVAL= int (cfg['app'].get('MQTT_KEEPALIVE_INTERVAL',MQTT_KEEPALIVE_INTERVAL) )
DOMOTICZ_IN_TOPIC= cfg['app'].get('DOMOTICZ_IN_TOPIC',DOMOTICZ_IN_TOPIC)



#for sec in cfg.sections():
 #   print('sec=',sec)
  #  opts= cfg.options(sec)
   # print('opts=',opts)
   # for o in opts:
    #    print('o=',o) 

#    if sec == 'mqtt_topics':
#        MQTT_TOPICS= cfg.options(sec)
##        print('MQTT_TOPICS=',MQTT_TOPICS)
        
#    elif sec = 'map_devices' :
#        opts= cfg.options(sec)
#        print('opts=',opts)
#        for o in opts:
#            d_map[o]= o.getint(sec,o 
            
            







#d_map['DS1']=2


#print("dmap=",d_map)
#for i in d_map :
#  print (i)
#  print(d_map[i])
#print (d_map['DS3'])


#print(MQTT_MSG)
# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect with MQTT Broker
print(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# Loop forever
mqttc.loop_forever()