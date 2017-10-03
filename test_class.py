
import time
import threading
from time import ctime

class A(object):
    def __init__(self):
        print('a init')
        self.ch = 1
        return super(A, self).__init__()
    
    def anormal(self):
        print(self.ch)
        
class B(object):
    a = A()
    def __init__(self):
        print('b init')
        
    def __new__(cls):
        print('new')
        return super(B, cls).__new__(cls)
    @staticmethod
    def s1():
        print('static')
    @classmethod
    def c1(cls):
        print('class method')

    def normal(self):
        print('normol')

    def __del__(self):
        print('del')
    
if __name__ == "__main__":
    
    print('t')
    
    
