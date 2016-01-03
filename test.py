import smtplib

fo = open("secure.cfg", "rb")
test = fo.read();

print test
datalist = test.split(',')
print datalist[2]

to = 'icabaad@gmail.com'
gmail_user = 'icabaad@gmail.com'
gmail_pwd = datalist[0];
print gmail_pwd

print test
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
print header
msg = header + '\n this is test msg from danger.com \n\n'
smtpserver.sendmail(gmail_user, to, msg)
print 'done!'
smtpserver.close()
