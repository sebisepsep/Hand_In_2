import numpy as np

#version for the integral without prefactors!
def nx2(x):
    return ((x)**(2.4-1))*np.exp(-(x/0.25)**1.6)

#integration
#trapezoid rule
def trap(func,a,b,N): #a=mini, b = maxi
    h = (b-a)/N
    x = np.linspace(a,b,N+1)
    result = (func(a)+func(b))*0.5
    for element in x[1:N-1]: 
        result += func(element)
    result = result*h
    return result 

#romberg integration
def romberg(func, mini, maxi, m): #a=mini, b = maxi
    h = maxi - mini
    r = np.zeros(m)
    r[0] = trap(func,mini,maxi,1)
    
    #step 4
    Np = 1
    for i in range(1,m): 
        #step 5
        delta = h 
        h = 0.5*h
        x = mini + h #a = mini
        for _ in range(Np): 
            r[i] = r[i] + func(x)
            x = x + delta

        #step 6
        r[i] = 0.5*(r[i-1]+ delta*r[i])
        #then double Np
        Np *=2
        
    #step 8
    Np = 1
    for i in range(1,m):
        #step 9
        Np *= 4
        for j in range(m-i):
            r[j] = (Np*r[j+1]-r[j])/(Np-1)
            
    return r[0]

#calculation A
mini = 0
maxi = 5
m = 10 #seemed to be a good choice
k = 4**(2.4-3)*4*np.pi*romberg(nx2, mini, maxi, m)
A = 1/k

#safe data  
with open('value.txt', 'w') as f:
    f.write(str(A))
    
np.save("a.npy",A)