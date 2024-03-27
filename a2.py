import numpy as np
import matplotlib.pyplot as plt

zz = 0.015
aa = 0.684/0.0416 + (2*np.log(zz))#+ 4* np.log(10)
bb = 0.929*10**4/0.0416

def f(t):
    return  (aa - np.log(t/10**4))*t - bb 

def central(function,x,h):
    return (function(x+h)-function(x-h))/2/h

# newton raphson method
interval = np.array([1,10**7])
xa = (interval[1]-interval[0])*0.5
h = 0.01
i = 0

while True:
    xa = xa - 10**(-0.5)*f(xa)/central(f,xa,h)
    if abs(f(xa)) < 10**(-10):
        break
    i += 1
    
with open("2a_res.txt", "w") as file:
    file.write(f"root is at x_0 = {round(xa)}, f(x_0) = {round(f(xa), 11)}, after {i} iteration")