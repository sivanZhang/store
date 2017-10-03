
import time
import threading
from time import ctime

class ProductManager(threading.Thread):

    __mutext__ = 1
    def run(self):
        global num 
        
        if lock.acquire(1):
            print('start') 
            num = num +1
            time.sleep(1)
            print(str(num )+'-')
            lock.release()
        
    def reduce(self):
        """减少库存"""
        global num 
        #lock = threading.Lock()
        #lock.acquire(10)
        time.sleep(2)
        num = num +1
        #lock.release()
        print(str(num )+'-')
        
        
    def reduce2(self):
        """减少库存"""
        print(ctime(),'reduce2')
       
        
            
          
    def __call__(self):
        print('__call__')
        apply(self.reduce)
 
        print(ctime())
num = 0
lock = threading.Lock()
if __name__ == "__main__":
    
    i = 0
    start = time.ctime()
    while i< 100000:
        lock.acquire()
         
        i += 1
        lock.release()

    print(start, time.ctime())
    
    print('done')
    
