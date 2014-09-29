# main.py, in general, run this.
# This work is protected under the terms of the GNU GPL v2.0 license.
# (c) Benjamin Wengert 2014

from threading import Timer
from opelqueue import queue
import os
from sendtext import sendtext
import getpass
import time

msgs=[]

def cls():
    os.system(['clear','cls'][os.name == 'nt']) # Grabbed this clever snippet from popcnt on StackOverflow

def pause():
    os.system(['read -p "Press any key to continue . . . "','pause'][os.name == 'nt']) # Made this one myself

print "This work is protected under the terms of the GNU GPL v2.0 license.\n(c) Benjamin Wengert 2014\n\n"
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

rmq = q.getqbyfield('room',p['room'])
pos = 1+q.findpos(p,rmq)
rmq = q.getqbyfield('room',p['room'])
msgs.append( str(time.strftime('%a %m/%d %I:%M:%S %p\n',time.localtime())+'%s is in position %i in the room queue.' % (p['name'],pos)) )
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
            
            msgs.append( str(time.strftime('%a %m/%d %I:%M:%S %p\n',time.localtime())+'%s has moved from %i to %i in the room queue.' % (p['name'],pos,currpos)) )
            
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
        msgs.append( str(time.strftime('%a %m/%d %I:%M:%S %p\n',time.localtime())+'%s has been removed from the queue.' % (p['name'],pos,currpos)) )
        text.send(msgs[-1:][0])
        pause()

rfsend()