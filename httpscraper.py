#! /usr/bin/env python
import smtplib
import re
import requests
import MySQLdb
from phant import Phant
import httplib

# secret file parse
file = open("secure.cfg", "rb")
textstr = file.read()
# file format dbname,dbuser,dbpass,emailpass,phantprivkey,utoobkey,
# print textstr
datalist = textstr.split(',')
# print datalist[0:6]
# print datalist[5]
file.close()

# mysql details
db = MySQLdb.connect(host='192.168.0.2', db=datalist[0], user=datalist[1], passwd=datalist[2])
cursor = db.cursor()

#EMONCMS details
homedomain = "dangerproxy:8080"
apikey = 'da3ae5f01b1245c3360ef85ddd8fb451'
payload = 'string'
conn = httplib.HTTPConnection(homedomain)

# phant server details
p = Phant('xR32G9R4KXTjDVonKVa9', 'danger', 'bigmong', 'gigs', 'cooperx', private_key=datalist[4])
users = ('theDanger', 'BigMong', 'Gigs', 'CooperX')  # Usernames go here
payload = [0, 0, 0, 0]  # empty list
payloader = 'p'  # return var
index = 0  # increment list

# utoobs
# url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=' + username + '&key=' + key
username = 'Icabaad'
key = datalist[5]
utooblist = [0, 0, 0]


# Sends Email
def send_mail(subject):
    to = 'icabaad@gmail.com'
    gmail_user = 'icabaad@gmail.com'
    gmail_pwd = datalist[3]
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n\n' + subject + '\n'
    print header
    msg = header + '\n this is test msg from danger.com \n\n'
    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()


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
#    parse = html2.split(":")
    parse = html2.split("\"")
#print 'parse ', parse
#print 'Length', len(parse)
#print 'strip', parse[37:]
    totalwatched = parse[37]
    totalsubs = parse[45]
    totalvids = parse[51]
#    relist = re.findall("\d{2,}", html2)
#    print relist
    # print relist[23]
    # print relist[25]
    # print relist[26]
 #   totalwatched = relist[0]
 #   totalsubs = relist[1]
 #   totalvids = relist[2]
 #   if (totalwatched < 9000): print 'The UToobs have shuffled!'

    return totalwatched, totalsubs, totalvids


try:
    # loop through users until done
    for user in users:
        payloader = get_tinyrssusr_data(user)
        # print user, payloader
        payload[index] = payloader
        index += 1

    print payload[0:4]
    index = 0
    p.log(payload[0], payload[1], payload[2], payload[3])  # log with phant server
    # print(p.remaining_bytes, p.cap)
    # data = p.get()
    print 'TinyRSS Scrape Complete'
except:
    print 'Unable to Scrape TinyRSS'
    send_mail('Unable to Scrape TinyRSS')

try:
    utooblist = get_utoob_stats(username, key)
    print 'Utoob: Watches: %s Subs: %s Vids: %s' % utooblist
    print 'UToob Scrape Complete'

except:
    print 'Unable to Scrape the UToobs'
    send_mail('Unable to Scrape Utoobs')

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO tblTinyRSS(TheDanger, BigMong, Gigs, CooperX) \
VALUES ('%s', '%s', '%s', '%s')" % \
      (payload[0], payload[1], payload[2], payload[3])

if (utooblist[0] > 9000):
    sql2 = "INSERT INTO tblUToob(Views, Subscribers, Videos) \
    VALUES ('%s', '%s', '%s')" % (utooblist[0], utooblist[1], utooblist[2])
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
    print "SQL Error"
    send_mail('Unable to Save to MySQL')

#Post to EmonCMS locally
payload = '{' + "TheDangerRSS:%s,BigMongRSS:%s,GigsRSS:%s,CooperX:%s" % (payload[0], payload[1], payload[2], payload[3]) + '}'
print payload
try:
    conn.request("GET", "/emoncms/input/post.json?node=1&apikey=" + apikey + "&json=" + payload)
    response = conn.getresponse()
    conn.close()
except (httplib.HTTPException, socket.error) as ex:
    print "Error: %s" % ex

payload = '{' + "Views:%s,Subscribers:%s,Videos:%s" % (utooblist) + '}'
print payload
try:
    conn.request("GET", "/emoncms/input/post.json?node=1&apikey=" + apikey + "&json=" + payload)
    response = conn.getresponse()
    conn.close()
except (httplib.HTTPException, socket.error) as ex:
    print "Error: %s" % ex