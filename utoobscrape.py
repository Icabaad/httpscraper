import requests
import re


url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=icabaad&key=AIzaSyDwvTdI4z6bJW7AkVamwVvl-9uO3ChxEac'
response = requests.get(url)
html = response.content

print html

parse = html.split(":")
print 'parse ', parse

#[int(s) for s in html.split() if s.isdigit()]
#bang = re.sub('/D+', '', html)
relist = re.findall('\d{2,}', html)
print 'parse2 ', relist
print 'parse3 ', bang


#print parse[15]
#print 'gap'
#print parse[14]
#print parse[9]

#print relist
#print relist[23]
#print relist[25]
#print relist[26]
#totalwatched = relist[23]
#totalsubs = relist [25]
#totalvids = [27]
#print parse[9]
#print parse[11]

    #list = html.split(';')
    # print list[0:2]
   # payloader = str(list[0])
    # payload[0] = payloader
    # print payloader
   # return payloader