"""This module contains a function for testing the speed of a function which solve Ax=b
usage:   import gausstest
         gausstest.speed(myfunction) # optional second argument, maximum size n
Here myfunction takes arguments A,b,"""
import timeit,time,gc
from statistics import mean,stdev
from random import seed,random

def randProb(n):
    "Returns a randomly generated n x n matrix A (as a dictionary) and right hand side vector b (as a list)."
    n = int(n)
    assert n > 0
    N = range(n)
    return dict( ((i,j), random()) for i in N for j in N), [random() for i in N]

def speed(method,maxSize=400):
    seed(123456) # fix some arbitrary seed so we keep generating the same data
    randP = lambda n : randProb(n) # add randProb to locals() namespace
    prev,n = 0.0, 50
    gc.disable()
    while n <= maxSize:
        gc.collect() # manual cleanout of garbage before each repeat
        t = timeit.repeat(stmt="method(A,b)",setup=f"A,b=randP({n})",
                      timer=time.process_time,repeat=5,number=1,globals=locals())
        print("%4d %10.4f σ=%.2f sec" % (n,mean(t),stdev(t)),"(x %.2f)"%(mean(t)/prev) if prev > 0 else "")
        prev = mean(t)
        n *= 2
    gc.enable()
