import serial
import httplib
import MySQLdb
import socket
import datetime
from time import sleep

ser = serial.Serial('/dev/ttyAMA0', 19200, timeout=0)  # RaspPi GPIO PIN serial
# ser = serial.Serial('/dev/ttyACM1', 9600) #RaspPi USB port
# conn = MySQLdb.connect( host='192.168.0.32', db='SensorDB', user='SensorNet', passwd='netsensor' )
# cursor = conn.cursor()
powercount = 0
errorcount = 0
minutecount = 0
payload = 'string'
apikey = 'da3ae5f01b1245c3360ef85ddd8fb451'
apikey2 = 'ebd4f194e60f6e8694f56aa48b094ddb'
homedomain = "dangerproxy:8080"
hostdomain = "emoncms.org"
conn = httplib.HTTPConnection(homedomain)
# conn2 = httplib.HTTPConnection(hostdomain) #Falling over Script when Net not connected? 08-10-2015

while True:
    #    data = ser.read(9999).strip("\r\n") #Reads upto 9999 bytes
    data = ser.readline().strip("\r\n")  # reads a line until /n is reached

    sleep(2.0)
    if len(data) >= 100:
        parsed = data.split(",")
        datalist = data.split(',')
        print 'Serial Packet Length:', len(data), 'Length:', len(datalist)
        print 'Got:', data
        print 'parsed:', parsed

        if len(datalist) == 10:
            print '***Power Reading Received!***'
            powercount += 1
            print 'Power Count: ', powercount
            print 'Error Count: ', errorcount
            payload = str(datalist).strip('[]')
            payload = ','.join(map(str, datalist))
            #            print payload
            payload = '{' + payload + '}'
            print payload
            try:
                conn.request("GET", "/emoncms/input/post.json?node=1&apikey=" + apikey + "&json=" + payload)
                response = conn.getresponse()
                #print 'power', homedomain, response.read(), response.status(), response.reason()
                #                conn2.request("GET", "/input/post.json?json="+payload+"&apikey="+apikey2)
                #                response = conn2.getresponse()
                #                print hostdomain, response.read()
                conn.close()
            except (httplib.HTTPException, socket.error) as ex:
                print "Error: %s" % ex

        elif len(datalist) == 23:
            print '***One Minute Update Received***'
            #            for x in datalist[0:20]: print x, ""
            minutecount += 1
            print 'Minute Count: ', minutecount
            print 'Error Count: ', errorcount
            #            print str(datalist).strip('[]')
            payload = str(datalist).strip('[]')
            payload = ','.join(map(str, datalist))
            #            print payload
            payload = '{' + payload + '}'
            print payload
            try:
                conn.request("GET", "/emoncms/input/post.json?node=1&apikey=" + apikey + "&json=" + payload)
                response = conn.getresponse()
                #print homedomain, response.read(), response.status(), response.reason()
                #                conn2.request("GET", "/input/post.json?apikey="+apikey2+"&json="+payload)
                #                response = conn2.getresponse()
                #                print 'emoncms.org', response.read()
                conn.close()
            except (httplib.HTTPException, socket.error) as ex:
                print "Error: %s" % ex

        else:
            print 'XXXXXRogue Serial String recieved!XXXXX'
            print datalist
            errorcount += 1
            print 'Error Count: ', errorcount

            # second sub parse into readable format
            #   data2 = datalist.split(':')
            #  print data2[0,2,4], '=', data2[1,3,5]


            # Prepare SQL query to INSERT a record into the database.
            # sql = "INSERT INTO tblSensorData(fldCommsMotion, fldCommsTemp, fldCommsBarometer, fldCommsHumidity, fldCommsLux, fldXbee1Temp, fldXbee1Volt, fldXbee1Battery, fldXbee1SolarV, fldTotalPowerUse, fldHeatuse, fldLightPower) \
            # VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
            # (datalist[0], datalist[1], datalist[2], datalist[3], datalist[4], datalist[5], datalist[6], datalist[7], datalist[8], datalist[9], datalist[10], datalist[11])
            #  print"sql ready for execution"
            # try:
            # Execute the SQL command
            ##   print"SQL Injected!"
            #        count = count + 1
            #        print 'SQL Update Count:', count
            #       results = cursor.fetchall()
            #       print "SQL lookup:", results
            # Commit your changes in the database
            #   conn.commit()

            #    else:
            #       if len(data) > 1 and < 50
            #       print "Serial Packet Out of Bounds"
            # except:
            # Rollback in case there is any error
            # conn.rollback()
# conn.close()
#

# sleep(1)
print 'not blocked'
ser.close()
conn.close()

