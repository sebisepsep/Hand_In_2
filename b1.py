import numpy as np
import matplotlib.pyplot as plt

A = np.load("a.npy")

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
    
def n_func(x):
    #sat=100
    #a=2.4
    #b=0.25
    #c=1.6
    #return A*sat*b**(3-a)*x**(a-1)*np.exp(-(x/b)**c)
    return A*100*0.25**(3-2.4)*x**(2.4-1)*np.exp(-(x/0.25)**1.6)

#provides the number of galaxies in area [x,x+h]
def N_func(x): #100p(x)dx = N(x)dx
    h = 5/1000 #1000 parts I use this value later as well
    m = 5 
    #multiplied by 4 \pi! = integrated over solid angle!
    return 4*np.pi*romberg(n_func, x, x+h, m)

def p_func(x):
    return N_func(x)/100

#sampling 10.000 points
#first starting with a random number generator

#to reduce number to 64bit 
def bit64(x):
    return x & 0xFFFFFFFFFFFFFFFF

#64 bit XOR shift method
def xor(x):
    a1 = 21
    a2 = 35
    a3 = 4

    x = x ^ (x>>a1)
    x = x ^ (x<<a2)
    x = x ^ (x>>a3)
    return bit64(x)

#Uniform RNG range 0-1
#possible to change iterations and seed
def uxor(N,m): 
    seed = 4 + m
    for i in range(1,N):
        seed = xor(seed)
    return (seed%100)/100

#slice sampling:
#initial guess 
x = uxor(2,4) * 5 
#numer of samplings
N = 10000

xpart = np.linspace(0,5,1000) # 1000, because I have choosen 5/1000 before at integration!
ypart = np.array([p_func(element) for element in xpart]) #p(xpart)
N_values = 100*ypart #N(xpart)

xsamp = np.zeros(N)


for k in range(N):
    #generate y
    y = uxor(k%10,10*k) * p_func(x)
    #trying to get random numbers by changing seed and # of iterations
    #without bringing N to high to reduce total time 

    #using p^-1(y) 
    s = xpart * (ypart >= y) 

    #creates an array with all non zero x values under the curve
    nonzero = np.array([])
    for element in s:
        if element != 0:
            nonzero = np.append(nonzero,element)


    #choosing a random element from the slice
    val = int(uxor(k%7,k)*len(nonzero))
    x = nonzero[val]

    #adding values to array, so that I can print it later :)
    xsamp[k] = x
    
np.save("sample.npy", xsamp)


plt.plot(xpart, N_values, label ="N(x)", color = "red")
edges = np.logspace(np.log10(1e-4), np.log10(5), 20 + 1)
# Calculate histogram
hist, b_edges = np.histogram(xsamp, bins=edges, density=False)
width = b_edges[1:]-b_edges[:len(b_edges)-1]
# Normalize each bin by its width
hist = hist / width /10000 #correct for offset and width
plt.bar(b_edges[:-1], hist, width= width, align='edge',label ='Satellite galaxies')

plt.ylim(10**(-3), 10)
plt.xlim(10**-4, 5)
plt.xlabel("virial radius x")
plt.ylabel("Number of galaxies N(x)")
plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.savefig('my_solution_1b.png')
