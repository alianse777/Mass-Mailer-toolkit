from tkinter import *
import tkinter.filedialog, tkinter.messagebox
from threading import Thread
from _sender import Sender
import numpy as np

class GUI():
   def __init__(self):
      """ We are going to show GUI """
      self.root = Tk()
      self.root.geometry("700x400")
      self.root.wm_title("MM toolkit v1.0")
      self.status = StringVar()
      self.filename = StringVar()
      self.smtpfilename = StringVar()
      self.subj = StringVar()
      self.msg_from = StringVar()
      self.count = StringVar()
      self.count.set("Emails send per SMTP: 0")
      self.pack()
      self.status.set("Status: waiting")
      self.root.mainloop()

   def pack(self):
      """ Pack elements """
      ss = Frame(self.root, bg="white")
      start = Button(ss,text="START",fg="blue",width=6,command=self.spam)
      self.pausebtn = Button(ss,text="PAUSE",fg="blue",width=6,command=self.pause)
      stop = Button(ss, text="STOP",fg="blue",width=6,command=self.stop)
      status = Label(ss, textvariable=self.status)
      count = Label(ss, textvariable=self.count)
      ss.pack(side=RIGHT)
      start.pack()
      self.pausebtn.pack()
      status.pack(side=BOTTOM)
      count.pack(side=BOTTOM)
      stop.pack(side=BOTTOM)

      # Another frame
      sett = Frame(self.root)
      name = Entry(sett,bg="white", textvariable=self.msg_from)
      namell = Label(sett,text="Send emails from:")
      subj = Entry(sett,bg="white", textvariable=self.subj)
      subjll = Label(sett, text="Subject:")
      self.text = Text(sett,bg="white",height=10,width=50)
      textll = Label(sett,text="Email text:")
      filebtn = Button(sett,text="Select a email list", command=self.openlist)
      filell = Label(sett,textvariable=self.filename)
      smtpbtn = Button(sett,text="Select a SMTP list", command=self.opensmtplist)
      smtpll = Label(sett,textvariable=self.smtpfilename)
      sett.pack()
      namell.pack()
      name.pack()
      subjll.pack()
      subj.pack()
      textll.pack()
      self.text.pack()
      filebtn.pack()
      filell.pack()
      smtpbtn.pack()
      smtpll.pack()

   def openlist(self):
      """ Get and open file with emails """
      options = {}
      options['title'] = 'Select file with emails'
      self.list = tkinter.filedialog.askopenfilename(**options)
      if self.list:
         try:
            self.emailscount = sum(1 for line in open(self.list))
            self.filename.set("File: %s / %s Emails" % (self.list,self.emailscount))
         except:
            tkinter.messagebox.showinfo("Error", "Can not load emails!")

   def opensmtplist(self):
      """ Get and open file with SMTPs """
      options = {}
      options['title'] = "Select file with smtp's (password:login@host:port one per line)"
      self.smtplist = tkinter.filedialog.askopenfilename(**options)
      if self.smtplist:
         try:
            self.smtpscount = sum(1 for line in open(self.smtplist))
            self.smtpfilename.set("File: %s / %s SMTP's" % (self.smtplist,self.smtpscount))
         except:
            tkinter.messagebox.showinfo("Error", "Can not load SMTP servers!")

   def spam(self):
      """ Fire! """
      t = Thread(target=self.run)
      t.start()

   def stop(self):
      self.status.set("Status: finished")
   def pause(self):
      if self.status.get() != "Status: waiting":
         self.pausebtn.configure(text="RESUME",command=self.resume)
         self.status.set("Status: paused")
   def resume(self):
      self.pausebtn.configure(text="PAUSE",command=self.pause)
      self.status.set("Status: running")

   def run(self):
      """ start mailing """
      subj = self.subj.get()
      text = self.text.get('1.0', 'end-1c')
      msg_from = self.msg_from.get()
      if not subj:
         tkinter.messagebox.showinfo("Error", "Please fill the message subject!")
      elif not text:
         tkinter.messagebox.showinfo("Error", "Please fill the message text!")
      elif not msg_from:
         tkinter.messagebox.showinfo("Error", "Please type the sender's email!")
      elif not self.list:
         tkinter.messagebox.showinfo("Error", "Please select emails list!")
      elif not self.smtplist:
         tkinter.messagebox.showinfo("Error", "Please select SMTP list!")
      elif self.status.get() == "Status: running":
         tkinter.messagebox.showinfo("Error", "Already running!")
      else:
         if "<" not in text or ">" not in text:
            tkinter.messagebox.showinfo("Warning!", "There is no html tags in your text. This can cause mails to get into Spam.")
         self.count.set("Connecting...")
         self.status.set("Status: running")

         smtps = open(self.smtplist, "r").read()
         emails = open(self.list,'r').read().split()
         insmtp = len(emails)/self.smtpscount
         smtps = smtps.split("\n")
         i =0
         for smtp in smtps:
            if smtp:
               try:
                  smtp = smtp.split(":")
                  s = Sender(smtphost=smtp[2],smtpport=smtp[3],username=smtp[1],password=smtp[0])
                  s.format(subject=subj,body=text,msg_from=msg_from)
                  s.send(emails[int(insmtp)*i:int(insmtp)*i + int(insmtp)], self.status,self.count)
                  i+=1
               except KeyboardInterrupt:
                  pass
         self.status.set("Status: finished")

if __name__ == "__main__":
   GUI()
