import smtplib, sys, os

def check(host,port,log,pas,fl):
   try:
      s = smtplib.SMTP(host,port, timeout=10)
      s.ehlo()
      s.starttls()
      s.ehlo()
      s.login(log,pas)
      fl.write("{0}:{1}:{2}:{3}\n".format(pas,log,host,port))
      s.close()
   except smtplib.SMTPAuthenticationError:
      print(host,"Incorrect login/password")
   except smtplib.SMTPServerDisconnected:
      print(host,"Unable to connect")

# This is used to clean result file.
#os.remove("checked.txt")

fl = open("checked.txt", "a")
if len(sys.argv) < 2:
   print ("Usage: smtpchecker.py smtps.txt")
else:
   with open(sys.argv[1],'r') as smtps:
      for line in smtps:
         smtp = line.split(":")
         check(smtp[2],int(smtp[3]),smtp[1],smtp[0],fl)
fl.close()
