# Benjamin Wengert - OpelQueue - Loads data off of the Virginia Tech OpEL's website
# Copyright (C) 2014  Benjamin Wengert

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import smtplib
class sendtext:
    def __init__(self,pid,pwd,num,carrier):
        self.pid=pid
        self.pwd=pwd
        self.num=num
        self.carrier=carrier
        self.domains={'t':'@tmomail.net','v':'@vtext.com','a':'@txt.att.net','s':'@messaging.sprintpcs.com','vm':'@vmobl.com'}
        
    def send(self, msg):
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(self.pid+'@vt.edu', self.pwd)
        smtpserver.sendmail(self.pid+'@vt.edu', self.num+self.domains[self.carrier], msg)
        smtpserver.close()