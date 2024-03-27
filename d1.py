import numpy as np

A = np.load("a.npy")
Nsat=100
a=2.4
b=0.25
c=1.6

def n(x):
    return A*Nsat*((x/b)**(a-3))*np.exp(-(x/b)**c)

def central(function,x,h):
    return (function(x+h)-function(x-h))/2/h

def ridder(func, x,m):
    #step 1 
    h = 0.1 #choosen by slides

    #step 2
    array = np.zeros(m)
    for i in range(m): 
        d = 2
        h = h / d
        array[i] = central(func,x,h)
        
    #step 3
    for k in range(m):
        for i in range(m-1-k):
            j = i+1
            array[i] = (d**(2*j)*array[j]-array[i])/(d**(2*j)-1)
    return array[0]

threshold = 10**(-9)
delta = np.array([])
i = 1
while True:
    delta =  np.append(delta,abs(ridder(n,1,i)))
    if i >= 2:
        if abs(delta[-1] - delta[-2]) < threshold:
            #print(i)
            m_best = i
            break
    i += 1

#safe data  
with open('1d_m.txt', 'w') as f:
    f.write(str(i))
with open('1d_delta_m.txt', 'w') as f:
    f.write(str(ridder(n,1,m_best)))