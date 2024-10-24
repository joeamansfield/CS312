import random
from math import floor

def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):
    if y == 0:
        return 1
    z = mod_exp(x, floor(y/2), N)
    if y%2 == 0:
        return z**2%N
    else:
        return x*z**2%N
#log(y) time because each iteration cuts the y in half
	

def fprobability(k):
    return 1-(.5**k)
    #there is a maximum 50% chance of being wrong on any individual a
    


def mprobability(k):
    return 1-(.25**k)
    #the text said that there is at least a 75% chance of revealing a composite n for a given any a, so only a 25% chance of being wrong on any a


def fermat(N,k):
    for i in range(k):
        a = random.randint(1, N-1)
        if mod_exp(a, N-1, N) != 1: #function is log(n)
            return 'composite'
    return 'prime'
#function overall is going to be klog(n) time where k is the number of iterations chosen


def miller_rabin(N,k):
    n = N-1
    t = 0
    while n%2 == 0:
        t+=1
        n = n/2
    for i in range(0, k):
        a = random.randint(2, N-1)
        x = mod_exp(a, N-1, N)
        if x != 1:
            return 'composite'
        for i in range(0,t-1): #loop runs log(n) times because t is the number of times n could be cleanly divided in two
            x = mod_exp(x, 2, N)#function is log(n)
            if x == N-1:
                return 'composite'
    return 'prime'
#function overall will be k log(n) squared time
