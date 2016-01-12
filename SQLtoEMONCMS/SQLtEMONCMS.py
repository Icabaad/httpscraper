import MySQLdb
import httplib

file = open("secure.cfg", "rb")
textstr = file.read()
datalist = textstr.split(',')

file.close()

db = MySQLdb.connect(host='192.168.0.2', db=datalist[0], user=datalist[1], passwd=datalist[2])
cursor = db.cursor()

homedomain = "dangerproxy:8080"
apikey = 'da3ae5f01b1245c3360ef85ddd8fb451'
payload = 'string'

conn = httplib.HTTPConnection(homedomain)

sql = "SELECT Views, Subscribers, Videos FROM `tblUToob` ORDER BY id DESC LIMIT 1"
cursor.execute(sql)
result = cursor.fetchall()
print result
for row in result:
    Views = row[0]
    Subscribers = row[1]
    Videos = row[2]
    print "Views=%s,Subscribers=%s,Videos=%d" % \
    (Views, Subscribers, Videos )

# disconnect from server
db.close()
payload = '{' + "Views:%s,Subscribers:%s,Videos:%d" % (Views, Subscribers, Videos ) + '}'
print payload
try:
    conn.request("GET", "/emoncms/input/post.json?node=1&apikey=" + apikey + "&json=" + payload)
    response = conn.getresponse()
    conn.close()
except (httplib.HTTPException, socket.error) as ex:
    print "Error: %s" % ex