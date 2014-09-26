import smtplib
class sendtext:
    def __init__(self,pid,pwd,num,carrier):
        self.pid=pid
        self.pwd=pwd
        self.num=num
        self.domain={'t':'@tmomail.net','v':'@vtext.com','a':'txt.att.net','s':'@messaging.sprintpcs.com','vm':'@vmobl.com'}[carrier]
        
    def send(self, msg):
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(self.pid+'@vt.edu', self.pwd)
        smtpserver.sendmail(self.pid+'@vt.edu', self.num+self.domain, msg)
        smtpserver.close()