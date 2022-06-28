from gurux_dlms.GXByteBuffer import GXByteBuffer
import serial
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from binascii import unhexlify
import sys
import string
import paho.mqtt.client as mqtt
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from gurux_dlms.GXDLMSTranslatorMessage import GXDLMSTranslatorMessage
from bs4 import BeautifulSoup

# EVN Schluessel eingeben zB. "36C66639E48A8CA4D6BC8B282A793BBB"
evn_schluessel = "dein_Schluessel"

#MQTT Verwenden (True | False)
useMQTT = False
useMYSQL = True
useFILE = True

#MQTT Broker IP adresse Eingeben ohne Port!
mqttBroker = "192.168.1.10"
mqttuser =""
mqttpasswort = ""
#Aktuelle Werte auf Console ausgeben (True | False)
printValue = True

#Comport Config/Init
comport = "/dev/ttyUSB0"


#MQTT Init
if useMQTT:
    try:
        client = mqtt.Client("SmartMeter")
        client.username_pw_set(mqttuser, mqttpasswort)
        client.connect(mqttBroker, port=1883)
    except:
        print("Die Ip Adresse des Brokers ist falsch!")
        sys.exit()



tr = GXDLMSTranslator()
tr.blockCipherKey = GXByteBuffer(evn_schluessel)
tr.comments = True
ser = serial.Serial( port=comport,
         baudrate=2400,
         bytesize=serial.EIGHTBITS,
         parity=serial.PARITY_NONE,
)


while 1:
    daten = ser.read(size=282).hex()
    print(daten)

    msg = GXDLMSTranslatorMessage()
    msg.message = GXByteBuffer(daten)
    xml = ""
    pdu = GXByteBuffer()
    tr.completePdu = True
    while tr.findNextFrame(msg, pdu):
        pdu.clear()
        xml += tr.messageToXml(msg)

    #soup = BeautifulSoup(xml, 'lxml')
    soup = BeautifulSoup(xml, 'html.parser')

    results_32 = soup.find_all('uint32')
    results_16 = soup.find_all('uint16')
    #print(results_16)

    #Wirkenergie A+ in KiloWattstunden
    WirkenergieP = int(str(results_32)[16:16+8],16)/1000

    #Wirkenergie A- in KiloWattstunden
    WirkenergieN = int(str(results_32)[52:52+8],16)/1000


    #Momentanleistung P+ in Watt
    MomentanleistungP = int(str(results_32)[88:88+8],16)

    #Momentanleistung P- in Watt
    MomentanleistungN = int(str(results_32)[124:124+8],16)

    #Spannung L1 in Volt
    SpannungL1 = int(str(results_16)[16:20],16)/10

    #Spannung L2 in Volt
    SpannungL2 = int(str(results_16)[48:52],16)/10

    #Spannung L3 in Volt
    SpannungL3 = int(str(results_16)[80:84],16)/10



    #Strom L1 in Ampere
    StromL1 = int(str(results_16)[112:116],16)/100

    #Strom L2 in Ampere
    StromL2 = int(str(results_16)[144:148],16)/100

    #Strom L3 in Ampere
    StromL3 = int(str(results_16)[176:180],16)/100


    #Leistungsfaktor
    Leistungsfaktor = int(str(results_16)[208:212],16)/1000



    if printValue:
        print('Wirkenergie+: ' + str(WirkenergieP))
        print('Wirkenergie: ' + str(WirkenergieN))
        print('MomentanleistungP+: ' + str(MomentanleistungP))
        print('MomentanleistungP-: ' + str(MomentanleistungN))
        print('Spannung L1: ' + str(SpannungL1))
        print('Spannung L2: ' + str(SpannungL2))
        print('Spannung L3: ' + str(SpannungL3))
        print('Strom L1: ' + str(StromL1))
        print('Strom L2: ' + str(StromL2))
        print('Strom L3: ' + str(StromL3))
        print('Leistungsfaktor: ' + str(Leistungsfaktor))
        print('Momentanleistung: ' + str(MomentanleistungP-MomentanleistungN))
        print()
        print()


    #MQTT
    if useMQTT:
        connected = False
        while not connected:
            try:
                client.reconnect()
                connected = True
            except:
                print("Lost Connection to MQTT...Trying to reconnect in 2 Seconds")
                time.sleep(2)

        client.publish("Smartmeter/WirkenergieP", WirkenergieP)
        client.publish("Smartmeter/WirkenergieN", WirkenergieN)
        client.publish("Smartmeter/MomentanleistungP", MomentanleistungP)
        client.publish("Smartmeter/MomentanleistungN", MomentanleistungN)
        client.publish("Smartmeter/Momentanleistung", MomentanleistungP - MomentanleistungN)
        client.publish("Smartmeter/SpannungL1", SpannungL1)
        client.publish("Smartmeter/SpannungL2", SpannungL2)
        client.publish("Smartmeter/SpannungL3", SpannungL3)
        client.publish("Smartmeter/StromL1", StromL1)
        client.publish("Smartmeter/StromL2", StromL2)
        client.publish("Smartmeter/StromL3", StromL3)
        client.publish("Smartmeter/Leistungsfaktor", Leistungsfaktor)

        
    if useFILE:
        f = open("/run/smartmeter.html", "w")
        f.write("<html><head><title>Smartmeter</title> <meta http-equiv=\"refresh\" content=\"3\"> </head>  <body>  </body></html><pre>")
        f.write("Leistung   : " + str(MomentanleistungP - MomentanleistungN) + " W\n")
        f.write("Verbraucht : " + str(WirkenergieP) + "\n")
        f.write("Eingespeist: " + str(WirkenergieN) + "\n")
        f.write("L1 : " + str(SpannungL1) + "V " + str(StromL1)+ "A\n")
        f.write("L2 : " + str(SpannungL2) + "V " + str(StromL2)+ "A\n")
        f.write("L3 : " + str(SpannungL3) + "V " + str(StromL3)+ "A\n")
        f.close()
        
        
        
    if useMYSQL:
        import mysql.connector

        mydb = mysql.connector.connect(
          host="MYSQL_HOST",
          user="MYSQL_USER",
          password="MYSQL_PW",
          database="MYSQL_DB"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO TABELLENNAME (zeit, bezug, einspeisung, leistung, U_L1, U_L2, U_L3, I_L1, I_L2, I_L3, Leistungsfaktor) VALUES (utc_timestamp(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (WirkenergieP, WirkenergieN, MomentanleistungP - MomentanleistungN, SpannungL1, SpannungL2, SpannungL3, StromL1, StromL2, StromL3, Leistungsfaktor)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        
        
        
