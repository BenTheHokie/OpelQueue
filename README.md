OpelQueue
=========

Queue tracker for opel.ece.vt.edu. When main.py is run, the script will ask for your Virginia Tech PID and email password as well as phone number and carrier. When you have moved into the 3rd position (and all positions after that) within the room you have signed up for, the script will send you a text message notifying you.

##DISCLAIMER

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should receive a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

##How to Use

Ensure that BeautifulSoup is installed
Run main.py

##Note

This python script uses SMTP to deliver text messages to a phone. If you are uncomfortable with the use of SMTP, please do not use this script. I'm going to tell you right now, that I am not collecting your email and/or password. There's really no way I can prove this to you unless you look through the code. If you want to use this script, then use it and if not, then don't.

##Dependencies
BeautifulSoup - http://www.crummy.com/software/BeautifulSoup/

##Goals

1. Send a text via email when the student has moved into the 3rd position in the queue (for the specific room) and after all position changes after that
2. Tell the user how long they've been waiting
3. (Maybe ... probably not) Automatically add yourself to the queue

##How to Use opelqueue.py

```python
from opelqueue import queue
q=queue(pid) # Specify optional localpage variable if you would like to use your 
             # own queue page (helpful for debugging)
```

It is important to know that the complete queue variable is stored within `self.bigq`

###List of Functions
Function | Purpose | Use
 -------- | -------- | -------- 
`__init__` | Initialization function | When an instance of queue is created, `__init__` will pull the queue from the OpEL website and load it into `self.bigq`
`strq` | Turn a queue into a human-readable format | The function takes one list as an argument and makes it into a table and returns it as a string
`findbypid` | Gives you information about yourself | This function takes no arguments and returns the dictionary of the PID that you put in when you instanciated the queue. Raises IndexError if your PID could not be found.
`getqbyfield` | Filters the queue | Takes in two arguments. The first, `field`, takes in the field you want to sort by. The second `value` takes in the value to filter. For example, ```q.getqbyfield('room',222)``` will sort the big queue into a smaller queue containing only people signed up in room 222
`findbyname` | Finds someone by their name in the queue | Takes in one argument, `name`, and returns the dictionary of someone with that name in `self.bigq`

The remaining functions are relatively menial and used internally and have their purpose commented within the code.