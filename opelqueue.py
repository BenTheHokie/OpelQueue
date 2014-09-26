from bs4 import BeautifulSoup
import datetime
import time
import os
from threading import Timer

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

class queue:
    
    def data2dict(self,data): # extract data into a dictionary
        return {'time' : self.parsetime(data[0].string), 'room' : data[1].string , 'course' : data[2].string, 'vorq' : data[3].string.lower(), 'name' : data[4].string} # we parse the time into a datetime object so it can be subtracted from other times and formatted into text
    
    def findbypid(self):
        dlist = self.soup('tr', {'class':'hilite'})[0].find_all('td') #this comes out as a 1-element array ("[0]")so we need to get the first and only value then we have to navigate to each piece of information as an array ".find_all('td')"
        return self.data2dict(dlist)
    
    def findbyname(self,name):
        for person in self.bigq:
            if str(person['name'].lower()).translate(None,' .,!-')==str(name.lower()).translate(None,' .,!-'): # if the names are close enough (for example typed "John D." instead of "John D"), just accept it and give them the person and the data
                # something weird happened here. str.translate does not have the same functionality as unicode.translate
                return person
        return False
    
    def printperson(self,person): # TBH I don't even know why I have this in here.
        print "%s appears to be in room %s for a %s in %s" % (person['name'],person['room'],person['vorq'],person['course'])
    
    def __init__(self, pid, localpage = None): #We can use local storage as an input, just provide the directory
        self.pid=pid
        if localpage:
            f=open('page.htm','r') #if we want to use the local page, just pull it from the directory
            self.pgsrc=f.read()
            f.close()
            
        else:
            import urllib2
            url = 'https://secure.hosting.vt.edu/www.opel.ece.vt.edu/queue.php?pid='+self.pid
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'} 
            request = urllib2.Request(url, None, headers)
    
            response = urllib2.urlopen(request,None,5)
            
            self.pgsrc = response.read()
        
        self.refresh=True        
        
        self.soup=BeautifulSoup(self.pgsrc)
        self.bigqsrc = self.soup.find_all('table')[3].find_all('tr')
        self.bigqsrc=self.bigqsrc[1:] #cut out the table headers (they mess with the data)
        
        self.bigq=[]
        for person in self.bigqsrc:
            dlist=person.find_all('td') 
            self.bigq+=[self.data2dict(dlist)]
            
    
    def parsetime(self, timestr):
        return datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S') # Takes input in the style of the OpEL output eg, 2014-09-23 19:24:59
    
    def time2str(self, _time):
        return _time.strftime('%I:%M:%S %p').lstrip('0') #strip the leading zeros to give a more "natural" look to the time display
    
    def setspc(self, string, length, spacechar=' '): #set spacing (useful for prettifying tables)
        string=str(string)
        if len(string)>length:
            return string[:length]
        else:
            return string+spacechar*(length-len(string)) #basically returns a string with some spaces at a specified length
    
    def strq(self, q): # output a queue in a readable table
        # TODO: let the user input fields that they want to see in the output
        ts=13 # set some constants for the amount of spacing: time space, difference space, room space, course space... etc
        ds=8
        rs=10
        cs=8
        vs=10
        ns=20
        e='*empty*' # Empty constant string to cut down on physical code length (python needs constants)
        final='%s|%s|%s|%s|%s|%s\n'%( self.setspc('Time',ts) , self.setspc('Elapsed',ds) , self.setspc('Room',rs) , self.setspc('Class',cs) , self.setspc('VorQ',vs) , self.setspc('Name',ns) )
        final+='%s+%s+%s+%s+%s+%s\n'%('-'*ts,'-'*ds,'-'*rs,'-'*cs,'-'*vs,'-'*ns) # table line
        if len(q)==0:
            final+='%s|%s|%s|%s|%s|%s\n'%( self.setspc(e,ts) , self.setspc(e,ds) , self.setspc(e,rs) , self.setspc(e,cs) , self.setspc(e,vs) , self.setspc(e,ns) )
        else:
            for i in range(len(q)):
                tdiff=datetime.datetime.today()-q[i]['time']
                final+='%s|%s|%s|%s|%s|%s\n'%( self.setspc(self.time2str(q[i]['time']),ts) , self.setspc(str(datetime.timedelta(seconds=tdiff.seconds)),ds) , self.setspc(q[i]['room'],rs) , self.setspc(q[i]['course'],cs) , self.setspc(q[i]['vorq'],vs) , self.setspc(q[i]['name'],ns) )
        return final
    
    
    def getqbyfield(self, field, value):
        final = []
        value = str(value)
        if field.lower()=='class': #catch mistakes
            field='course'
        for p in self.bigq: #p stands for person
            if p[field]==value:
                final+=[p]
        return final
    
    def findpos(self, p, q): #p again stands for a person dictionary
        try:
            return q.index(p)
        except ValueError:
            return -1

def refreshprint(pid,q):
    if q.refresh:
        cls()
        q=queue(pid)
        print q.strq(q.bigq)
        t=Timer(10,refreshprint,args=[pid,q])
        t.start()

if __name__ == '__main__':
    pid=raw_input("Input your PID.\nPID: ")
    q=queue(pid)
    print q.strq(q.bigq)
    try:
        q.printperson(q.findbypid())
    except IndexError:
        print "You do not appear to be in the queue."
    t=Timer(10,refreshprint,args=[pid,q])
    t.start()