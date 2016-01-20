import json
import datetime
from dateutil.parser import parse
import MySQLdb
import os
import httplib

def deleteContent(fName):
    with open(fName, "w"):
        pass

#EMONCMS details
homedomain = "dangerproxy:8080"
apikey = 'da3ae5f01b1245c3360ef85ddd8fb451'
payload = 'string'
conn = httplib.HTTPConnection(homedomain)

db = MySQLdb.connect("192.168.0.2","SensorNet","netsensor","SensorDB")
cursor = db.cursor()
keynames = []
trial = []
playcount = 0
file_object = open('//dangernas/Scrapes/Lastfm/lastfmplay.txt', "rb")
lines = file_object.read( ).splitlines(  )
file_object.close()
#os.remove('//dangernas/Scrapes/Lastfm/lastfmplay.txt') #delete file

for line in lines:
    line = line.rstrip( )
    line = line.rstrip('/n')
    trial.append(json.loads(line))
    #print(trial)
#print (keynames)

# grabs date from dictionary and converts to MySQL format. Yes!
for x in trial:
    dt = parse(x.get('Date'))
    x['Date'] = (dt.strftime('%Y/%m/%d %H:%M:%S'));
    #print(x)
    keys = (x.keys())
    values = (x.values())
    sql = "INSERT INTO testtbl(%s, %s) VALUES ('%s', %s)" % (keys[0], keys[1], values[0], values[1]) #, values[1])
    #print(sql)
    playcount += 1

    try:
     # Execute the SQL command
        cursor.execute(sql)
     # Commit your changes in the database
        db.commit()
    except:
        print('No Jooce!!!')
        sql2 = "ALTER TABLE testtbl ADD %s INT;" % (keys[1]) #, keys[1])
        print(sql2)
        cursor.execute(sql2)
        cursor.execute(sql)
        db.commit()
    else:
        db.rollback()

    payload = '{' + "TracksPlayed:"+(str(playcount)) + '}'

print (playcount)
print (payload)

try:
    conn.request("GET", "/emoncms/input/post.json?node=1&apikey=" + apikey + "&json=" + payload)
    response = conn.getresponse()
    conn.close()
    playcount = 0
except (httplib.HTTPException, socket.error) as ex:
    print "Error: %s" % ex

deleteContent('//dangernas/Scrapes/Lastfm/lastfmplay.txt')
os.utime('//dangernas/Scrapes/Lastfm/lastfmplay.txt', None)



