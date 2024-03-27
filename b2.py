import numpy as np

ab = 5*10**-10 #cm**3 s**-1
zeta_cr = 10**-15 #s**-1
ne = np.array([10**-4,1,10**4]) #cm**-3
t_int = np.array([1,10**15]) #K
t_acc = 10**-10
AA = 5*10**-10 #erg
kb = 1.38*10**-23 *10**7 #erg/K
phi = 0.929

zz = 0.015
alpha = -0.54/10**(4*0.37)
beta = 0.684
gamma = 0.0416
delta = 1/(10**4*zz**2)
epsilon = AA * zeta_cr /ab / kb #NOT THE A FROM TASK 1!!!
zeta = 8.9*10**-26/ab/kb/10**4
eta = phi

#defining function
def f2(t,ne):
    return alpha * t**(1+0.37) * ne - ne * (beta - gamma*np.log(delta*t)) * t + epsilon + zeta*t + ne * eta 
#bisection
def bi_new(func, interval ,acc, number):
    oben = max(interval)
    unten = min(interval)
    mitte = round((oben - unten)/2)
    
    count= 0
    while True:            
        #upper interval    
        if  func(mitte) <= number <= func(oben):
            oben = oben
            unten = mitte
            mitte = mitte + ((oben - unten)/2)

        #lower interval
        if  func(unten) <= number < func(mitte):
            oben = mitte
            unten = unten
            mitte = mitte - ((oben - unten)/2)

        if abs(func(mitte)) < acc:
            #print(f"iterations = {count}")
            break
        #print(func(unten), func(oben))
        count += 1
    return mitte, func(mitte), count  #returns position

nee = 0
for i in range(3):    
    def f3(t):
        nee = ne[i] #iterating for different densities 
        return -f2(t,nee) 
    array = bi_new(f3, t_int , 10**-10, 0)
    
    with open(f"2b_res{i}.txt", "w") as file:
        file.write(f"The root is at x = {array[0]}, f(x) = {array[1]}, after {array[2]} iteration")
