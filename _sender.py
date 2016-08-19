#-*-coding: utf-8-*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, os, random, time


class Sender():
   def __init__(self,smtphost, smtpport,username,password):
      self.server = smtplib.SMTP(smtphost, int(smtpport), timeout=20)
      self.server.ehlo()
      self.server.starttls()
      self.server.ehlo()
      self.server.login(username, password)

   def format(self,subject,body,msg_from):
      self.msg_subject = subject.encode("utf-8").strip()
      self.body = body.encode('ascii', 'xmlcharrefreplace')
      self.msg_from = msg_from

   def randomize(self,body):
      try:
         parts = body.split("/~/")
         return parts[random.randint(0,len(parts)-1)].decode()
      except:
         return body.decode()

   def pack(self, to):
      msg = MIMEMultipart()
      msg['From'] = "<" +self.msg_from+ ">"
      msg['To'] = '<'+to+'>'
      msg['Message-Id'] = "<200601051641.31830.ab@gmail.com>"
      tm = time.gmtime()
      msg['Date'] = "%s (UTC)" % time.strftime("%a, %d %b %Y %T %z",time.gmtime())
      msg['Content-Type'] ="text/html; charset='UTF-8'"
      msg['Subject'] = self.msg_subject.decode()
      msg.attach(MIMEText(self.randomize(self.body), 'html'))
      return msg


   def send(self, emails, status,progress):
      count = len(emails)
      i = 0
      while 1:
         if status.get() != "Status: paused":
            email = emails[i]
            if email != "": 
               i += 1
               text = self.pack(email).as_string()
               self.server.sendmail(self.msg_from, email, text)
               progress.set("Emails send per SMTP: %s" % i)
               # time.sleep(60)
            else:
               i += 1
         if status.get() == "Status: finished" or i == count:
            break
