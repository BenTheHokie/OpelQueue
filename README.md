OpelQueue
=========

Queue tracker for opel.ece.vt.edu

##Goals
1. Send a text via email when the student has moved into the 3rd position in the queue (for the specific room) and after all position changes after that
2. Tell the user how long they've been waiting
3. (Maybe ... probably not) Automatically add yourself to the queue

##How to Use

Function | Purpose | Output
 -------- | -------- | -------- 
`__init__` | Initialization function | When an instance of queue is created, `__init__` will pull the queue from the OpEL website and load it into self.bigq
