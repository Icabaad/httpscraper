#V2 of recieving and parsing of serial data
import json
data1 = '{"temperature":100.25,"camel":200,"wombat":500}'

data = json.loads(data1)

print data
print data['camel']
print str(data)
print len(data)
print data.items()

#use this for %s!
print data.keys()
print data.values()
