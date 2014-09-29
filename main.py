# main.py, in general, run this.
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
# 
# Contact bwengert at vt dot edu

from threading import Timer
from opelqueue import queue
import os
from sendtext import sendtext
import getpass
import time
import datetime

msgs=[]

def cls():
    os.system(['clear','cls'][os.name == 'nt']) # Grabbed this clever snippet from popcnt on StackOverflow

def pause():
    os.system(['read -p "Press any key to continue . . . "','pause'][os.name == 'nt']) # Made this one myself

print "This program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, version 3\nCopyright (C) 2014  Benjamin Wengert\n\n"
pid = raw_input('Please input your PID.\nPID: ')
pwd = getpass.getpass('Please input your email password. Characters won\'t be shown.\nPWD: ')
pn = raw_input('Please input your phone number (w/o spaces or dashes).\nNumber: ')
carrier = raw_input('Please input your respective carrier.\nv: Verizon\na: AT&T\ns: Sprint\nt: T-Mobile\nvm: Virgin Mobile\nCarrier: ').lower()
text = sendtext(pid,pwd,pn,carrier)
while not(text.carrier in text.domains.keys()):
    cls()
    carrier = raw_input('Invalid input. Please input your respective carrier.\nv: Verizon\na: AT&T\ns: Sprint\nt: T-Mobile\nvm: Virgin Mobile\nCarrier: ').lower()
    text = sendtext(pid,pwd,pn,carrier)

print('Sending test text...')

msgs.append( str(time.strftime('%a %m/%d %I:%M:%S %p\nIf you have received this text, that means that texting for the OpEL queue is working!',time.localtime())) )
text.send(msgs[-1:][0])

print('Attempting to acquire queue...')
q=queue(pid)
cls()
print time.strftime('%A, %B %d, %Y  %I:%M:%S %p\n',time.localtime())
print q.strq(q.bigq)

p=False
try:
    p=q.findbypid()
except IndexError:
    name = raw_input("Your PID could not be found in the queue. Please input your name in the queue.\nName: ")
    p=q.findbyname(name)
    while not(p):
        cls()
        q=queue('',q.localpage) # reload the queue
        print time.strftime('%A, %B %d, %Y  %H:%M:%S\n',time.localtime())
        print q.strq(q.bigq)
        name = raw_input("Your name could not be found in the queue. Please input your name in the queue.\nName: ")
        p=q.findbyname(name)

rmq = q.getqbyfield('room',p['room']) # rmq is the queue of people only in the room that the specified person is in.
pos = 1+q.findpos(p,rmq)
rmq = q.getqbyfield('room',p['room'])
tdiff=datetime.datetime.today()-p['time'] # Finding the elapsed time

msgs.append( str(time.strftime('%a %m/%d %I:%M:%S %p\n',time.localtime())+'%s is in position %i in the room queue. Elapsed: %s' % (p['name'] , pos , str(datetime.timedelta(seconds=tdiff.seconds)).lstrip('0:'))) )
text.send(msgs[-1:][0])

def rfsend(): #refresh sending
    global msgs,pos,p,text,q
    
    cls()
    print time.strftime('%A, %B %d, %Y  %I:%M:%S %p\n',time.localtime())
    for i in msgs: # Display the list of sent messages
        print( 'SENT (%s): %s' % ( pn, i.replace('\n',' ') ) )
    print '\n'
    
    q=queue(q.pid,q.localpage)
    rmq = q.getqbyfield('room',p['room'])# room queue
    
    print q.strq(rmq)
    currpos = 1+q.findpos(p,rmq)
    if currpos:
        print "%s appears to be in room %s for a %s in %s and in position %i" % (p['name'],p['room'],p['vorq'],p['course'],pos)
        
        if (pos and (currpos != pos) and currpos<=3):
            tdiff=datetime.datetime.today()-p['time']

            msgs.append( str(time.strftime('%a %m/%d %I:%M:%S %p\n',time.localtime())+'%s has moved from %i to %i in the room queue. Elapsed: %s' % (p['name'],pos,currpos, str(datetime.timedelta(seconds=tdiff.seconds)).lstrip('0:') )) )
            
            print( '\nSENT (%s): %s' % ( pn, msgs[-1:][0].replace('\n',' ') ))
            
            text.send(msgs[-1:][0])
        
        pos=currpos
        t=Timer(10.0, rfsend)
        t.start()
        
    else:
        cls()
        print time.strftime('%A, %B %d, %Y  %I:%M:%S %p\n',time.localtime())
        print '\n'
        print q.strq(q.bigq)
        print '%s has been removed from the queue.' % p['name']
        tdiff=datetime.datetime.today()-p['time']

        msgs.append( str(time.strftime('%a %m/%d %I:%M:%S %p\n',time.localtime())+'%s has been removed from the queue. Elapsed: %s' % (p['name'] , pos , currpos , str(datetime.timedelta(seconds=tdiff.seconds)).lstrip('0:'))) )
        text.send(msgs[-1:][0])
        pause()

rfsend()