#! /usr/bin/env python

import requests
import MySQLdb
from phant import Phant

db = MySQLdb.connect(host='192.168.0.2', db='SensorDB', user='SensorNet', passwd='netsensor')
cursor = db.cursor()
p = Phant('xR32G9R4KXTjDVonKVa9', 'danger', 'bigmong', 'gigs', 'cooperx', private_key='ZaEpRZawDlS5wkXM0kJa')

users = ('theDanger', 'BigMong', 'Gigs', 'CooperX')
payload = [0, 0, 0, 0]
payloader = 'p'
index = 0


def get_usr_data(x):
    url = 'http://dangertech.org/rss/public.php?op=getUnread&fresh=1&login=' + x
    response = requests.get(url)
    html = response.content
    # print x, html
    list = html.split(';')
    # print list[0:2]
    payloader = str(list[0])
    # payload[0] = payloader
    # print payloader
    return payloader


for user in users:
    payloader = get_usr_data(user)
    print user, payloader
    payload[index] = payloader
    index += 1
print payload[0:5]
index = 0

p.log(payload[0], payload[1], payload[2], payload[3])
print(p.remaining_bytes, p.cap)
data = p.get()

print 'Complete'

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO tblTinyRSS(TheDanger, BigMong, Gigs, CooperX) \
VALUES ('%s', '%s', '%s', '%s')" % \
      (payload[0], payload[1], payload[2], payload[3])

print"sql ready for execution"

try:
    # Execute the SQL command
    print"SQL Injected!"
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
    print "Committed"
except:
    # Rollback in case there is any error
    db.rollback()
    print "Error"
db.close()
