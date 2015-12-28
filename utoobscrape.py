import requests
import re

url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=icabaad&key=AIzaSyDwvTdI4z6bJW7AkVamwVvl-9uO3ChxEac'
response = requests.get(url)
html = response.content

print html

parse = html.split(":")
print parse

#relist = re.split("[a-zA-Z: ,\n']+", html)
relist = re.findall("[0-9]+", html)
print relist
print relist[23]
print relist[25]
print relist[26]
totalwatched = relist[23]
totalsubs = relist [25]
totalvids = [27]
#print parse[9]
#print parse[11]

    #list = html.split(';')
    # print list[0:2]
   # payloader = str(list[0])
    # payload[0] = payloader
    # print payloader
   # return payloader