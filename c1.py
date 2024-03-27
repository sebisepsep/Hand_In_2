import numpy as np
import matplotlib.pyplot as plt

#select sort
def select(a):
    N = len(a)
    for i in range(N-1):
        imin = i
        for j in range(i+1,N):
            if a[j]<a[imin]:
                imin = j
        if imin != i: 
            val = a[i]
            a[i] = a[imin]
            a[imin] = val
    return a

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

values = np.load("sample.npy")
# we have 10000 samples and want 100 random out of them 
# they are not sorted at all -> divide it into 100 intervals and always pick one
step = 0
array = np.zeros(100)
for i in range(100):
    step = 100*i
    val = int(uxor(3,i)*100)
    array[i] = values[int(step+val)]

#sort 
chosen = select(array)

xmin, xmax = 10**-4, 5
sel = chosen
fig1c, ax = plt.subplots()
ax.plot(sel, np.arange(100))
ax.set(xscale='log', xlabel='Relative radius', ylabel='Cumulative number of galaxies',
       xlim=(xmin, xmax+xmin), ylim=(0, 100))
plt.savefig('my_solution_1c.png', dpi=600)