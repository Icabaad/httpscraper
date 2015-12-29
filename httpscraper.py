#! /usr/bin/env python

import re
import requests
import MySQLdb
from phant import Phant

# mysql details
db = MySQLdb.connect(host='192.168.0.2', db='SensorDB', user='SensorNet', passwd='netsensor')
cursor = db.cursor()

# phant server details
p = Phant('xR32G9R4KXTjDVonKVa9', 'danger', 'bigmong', 'gigs', 'cooperx', private_key='ZaEpRZawDlS5wkXM0kJa')

users = ('theDanger', 'BigMong', 'Gigs', 'CooperX')  # Usernames go here
payload = [0, 0, 0, 0]  # empty list
payloader = 'p'  # return var
index = 0  # increment list

# utoobs
#url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=' + username + '&key=' + key
username = 'Icabaad'
key = 'AIzaSyDwvTdI4z6bJW7AkVamwVvl-9uO3ChxEac'
utooblist = [0, 0, 0]


# scrapes data and puts in a list
def get_tinyrssusr_data(x):
    url = 'http://dangertech.org/rss/public.php?op=getUnread&fresh=1&login=' + x
    response = requests.get(url)
    html = response.content
    # print x, html
    list = html.split(';')
    # print list[0:2]
    payloader = str(list[0])
    # print payloader
    return payloader


def get_utoob_stats(user, apikey):
    utooburl = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=' + user + '&key=' + apikey
    response2 = requests.get(utooburl)
    html2 = response2.content
    parse = html2.split(":")
    relist = re.findall("[0-9]+", html2)
    #print relist
    #print relist[23]
    #print relist[25]
    #print relist[26]
    totalwatched = relist[23]
    totalsubs = relist[25]
    totalvids = relist[26]

    return totalwatched, totalsubs, totalvids


# loop through users until done
for user in users:
    payloader = get_tinyrssusr_data(user)
    #print user, payloader
    payload[index] = payloader
    index += 1
print payload[0:4]
index = 0

p.log(payload[0], payload[1], payload[2], payload[3])  # log with phant server
#print(p.remaining_bytes, p.cap)
#data = p.get()

print 'TinyRSS Scrape Complete'

utooblist = get_utoob_stats(username, key)
print 'Utoob: ', utooblist
print 'UToob Scrape Complete'

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO tblTinyRSS(TheDanger, BigMong, Gigs, CooperX) \
VALUES ('%s', '%s', '%s', '%s')" % \
      (payload[0], payload[1], payload[2], payload[3])
sql2 = "INSERT INTO tblUToob(Views, Subscribers, Videos) \
VALUES ('%s', '%s', '%s')" % \
      (utooblist[0], utooblist[1], utooblist[2])

print"sql ready for execution...."

try:
    # Execute the SQL command
    cursor.execute(sql)
    print"TinyRSS Injeculated!"
    cursor.execute(sql2)
    print"UToobs Injeculated!"
    # Commit your changes in the database
    db.commit()
    print "Committed"
except:
    # Rollback in case there is any error
    db.rollback()
    print "Error"
