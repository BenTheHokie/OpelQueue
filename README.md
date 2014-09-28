OpelQueue
=========

Queue tracker for opel.ece.vt.edu

##How to Use
Run main.py

##Goals
1. Send a text via email when the student has moved into the 3rd position in the queue (for the specific room) and after all position changes after that
2. Tell the user how long they've been waiting
3. (Maybe ... probably not) Automatically add yourself to the queue

##How to Use opelqueue.py

```python
from opelqueue import queue
q=queue(pid) # Specify optional localpage variable if you would like to use your own queue page (helpful for debugging)
```

It is important to know that the complete queue variable is stored within `self.bigq`

###List of Functions
Function | Purpose | Use
 -------- | -------- | -------- 
`__init__` | Initialization function | When an instance of queue is created, `__init__` will pull the queue from the OpEL website and load it into `self.bigq`
`strq` | Turn a string into a human-readable format | The function takes one list as an argument and makes it into a table and returns it as a string
`findbypid` | Gives you information about yourself | This function takes no arguments and returns the dictionary of the PID that you put in when you instanciated the queue. Raises IndexError if your PID could not be found.
`getqbyfield` | Filters the queue | Takes in two arguments. The first, `field`, takes in the field you want to sort by. The second `value` takes in the value to filter. For example, ```python q.getqbyfield('room',222)``` will sort the big queue into a smaller queue containing only people signed up in room 222
`findbyname` | Finds someone by their name in the queue | Takes in one argument, `name`, and returns the dictionary of someone with that name in `self.bigq`

The remaining functions are relatively menial and used internally and have their purpose commented within the code.
