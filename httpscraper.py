import requests
import sys
from phant import Phant

p = Phant('xR32G9R4KXTjDVonKVa9', 'danger', 'bigmong', 'gigs', 'cooperx', private_key='ZaEpRZawDlS5wkXM0kJa')

users = ('theDanger', 'BigMong', 'Gigs', 'CooperX')
# list = [1,2,3,4]
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







# print user, html

# datalist = html.split(';')
# print 'dl', datalist
# print datalist[0:2]
# parsed = html.split(";")
# print '2', parsed
# nocoma = str(parsed).strip('[]')
# print '3', nocoma
# nocoma = ','.join(map(str,datalist))
# print '4', nocoma
# print len(nocoma), len(datalist)
# total = datalist[0]
# new = datalist[1]
