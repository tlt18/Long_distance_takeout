import math
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib as mpl

#n is the number of order
n=12
#m is the number of food delivery man
m=6
center_num=3
m_p=m//center_num
#t is the crossover point
t=m//2
T_init=1000
T_min=0.1
alpha=0.9
loop_times=1000
v=500/3
vs=2000/3
t_pre=10
"""
center=[[1612.5,750.0],[2200,1500],[1200,2000]]
"""
center=[[3225.0, 1500.0], [4400, 3000], [2400, 4000]]

t_delay=20

#pc is the position of customers,pm is the position of merchants
pc=[0]*n
pm=[0]*n
order=[0]*m*2

#test data
limit=[10,10,10,20,20,20,30,30,30,40,50,50]
limit_max=[30,40,40,35,35,35,50,50,60,60,70,70]
"""
pm=[[725.0,2200.0],[1575.0,2587.5],[1062.5,875.0],[1650.0,1512.5],[637.5,1012.5],[1425.0,1887.5],[1650.0,1512.5],[2962.5,1150.0],[625.0,2562.5],[2137.5,1987.5],[2187.5,625.0],[912.5,687.5]]
pc=[[1925.0,1062.5],[1787.5,412.5],[737.5,425.0],[1837.5,2362.5],[1262.5,2075.5],[1687.5,1650.0],[737.5,1537.5],[1562.5,575.0],[1262.5,2075.0],[2712.5,1737.5],[2825.0,2425.0],[2625.0,2262.5]]
"""
pm=[[1450.0,4400.0],[3150.0,5175.0],[2125.0,1750.0],[3300.0,3025.0],[1275.0,2025.0],[2850.0,3775.0],[3300.0,3025.0],[5925.0,2300.0],[1250.0,5125.0],[4275.0,3975.0],[4375.0,1250.0],[1825.0,1375.0]]
pc=[[3850.0,2125.0],[3575.0,825.0],[1475.0,850.0],[3675.0,4725.0],[2525.0,4151.0],[3375.0,3300.0],[1475.0,3075.0],[3125.0,1150.0],[2525.0,4150.0],[5425.0,3475.0],[5650.0,4850.0],[5250.0,4525.0]]

#calculate the order belongs to which station
cenm=[0]*center_num
cenc=[0]*center_num
for i in range(3):
    cenm[i]=[]
    cenc[i]=[]
    

ordsta=[0]*n#order belongs to which center

def distance(a,b):
    e=abs(a[0]-b[0])+abs(a[1]-b[1])
    return e


for i in range(n):
    ordsta[i]=[0]*2
    am=distance(pm[i],center[0])
    bm=distance(pm[i],center[1])
    cm=distance(pm[i],center[2])
    ac=distance(pc[i],center[0])
    bc=distance(pc[i],center[1])
    cc=distance(pc[i],center[2])
    
    if((am<=bm)and(am<=cm)):
        cenm[0].append(i)
        ordsta[i][0]=0
    elif((bm<=am)and(bm<=cm)):
        cenm[1].append(i)
        ordsta[i][0]=1
    else:
        cenm[2].append(i)
        ordsta[i][0]=2
    
    if((ac<=bc)and(ac<=cc)):
        cenc[0].append(i)
        ordsta[i][1]=0
    elif((bc<=ac)and(bc<=cc)):
        cenc[1].append(i)
        ordsta[i][1]=1
    else:
        cenc[2].append(i)
        ordsta[i][1]=2


subt=[0]*n
for i in range(n):
    if ordsta[i][0]==ordsta[i][1]:
        subt[i]=0
    elif (((ordsta[i][0]==1) and (ordsta[i][1]==2))or((ordsta[i][0]==2)and(ordsta[i][1]==1))):
        subt[i]=math.sqrt((center[0][0]-center[1][0])**2+(center[0][1]-center[1][1])**2)/vs
    elif (((ordsta[i][0]==1) and (ordsta[i][1]==3))or((ordsta[i][0]==3)and(ordsta[i][1]==1))):
        subt[i]=math.sqrt((center[0][0]-center[2][0])**2+(center[0][1]-center[2][1])**2)/vs
    else:
        subt[i]=math.sqrt((center[2][0]-center[1][0])**2+(center[2][1]-center[1][1])**2)/vs
 


def mutation(a):
    length=len(a)
    b=[0]*length
    a_new=[0]*length
    for i in range(length):
        b[i]=a[i]
    random.shuffle(a)
    for i in range(length):
        a_new[i]=a[i]
        a[i]=b[i]
    return a_new
 

                    
def crossover(a,b):
    c=[0]*t
    for i in range(t):
        c[i]=a[i]
        a[i]=b[i]
        b[i]=c[i]
        

#time satisfaction
def satisfaction(li,Li,t):
    if t <=li:
        c=1
    elif li<t<=Li:
        c=(Li-t)/(Li-li)
    else:
        c=0
    return c


#fitness function
def fitness(center,limit,limit_max,order):
    sum=0
    distm=[0]*m
    timem=[0]*center_num
    distc=[0]*n
    ordert=[0]*n
    for i in range(m):
        length=n//m
        distm[i]=[0]*(length+1)
        distm[i][0]=distance(center[i//m_p],pm[order[i][0]])
        distm[i][length]=distance(pm[order[i][length-1]],center[i//m_p])
        distc[i]=[0]*(length+1)
        distc[i][0]=distance(center[i//m_p],pc[order[i][0]])
        distc[i][length]=distance(pc[order[i][length-1]],center[i//m_p])
        for j in range(1,length):
            distm[i][j]=distance(pm[order[i][j-1]],pm[order[i][j]])
            distc[i][j]=distance(pc[order[i][j-1]],pc[order[i][j]])
        t=[0]*n
        for j in range(length+1):
            t[i]=t[i]+distm[i][j]/v+distc[i][j]/(2*v)
            
    for i in range(center_num):
        timem[i]=max(t[i*m_p],t[i*m_p+1])
    
    for i in range(n):
        ordert[i]=subt[i]+timem[int(ordsta[i][0])]+t_delay+t_pre
 
        
    for i in range(n):
        sum=sum+satisfaction(limit[i],limit_max[i],ordert[i])

    return sum,ordert
        
 

    
        
                  
#initialization        
p=n//m
q=n%m
a=[0]*n
for i in range(n):
    a[i]=i
random.shuffle(a)

for i in range(2*m):
    order[i]=[0]*p
for i in range(m):
    for j in range(p):
        order[i][j]=cenm[i//m_p][(i%m_p)*p+j]
        order[i+m][j]=cenc[i//m_p][(i%m_p)*p+j]


   

#main program
T=T_init
fit_best_list=list()
fit_list=list()
fit_new_list=list()
ordert=[0]*n
ordert_best=[0]*n
order_best=order
fit_best,ordert_best=fitness(center,limit,limit_max,order_best)
fit_list.append(fit_best)
cenm_new=[0]*center_num
cenc_new=[0]*center_num
for i in range(center_num):
    cenm_new[i]=[]
    cenc_new[i]=[]
order_new=[0]*2*m
for i in range(2*m):
    order_new[i]=[0]*p


while T>T_min:
    times=0
    while(times<loop_times):
        fit,ordert=fitness(center,limit,limit_max,order)
        order_new=[0]*2*m
        for i in range(2*m):
            order_new[i]=[0]*p

        for i in range(center_num):
            temp=random.random()
            if temp>0.2:
                cenm_new[i]=mutation(cenm[i])
                cenc_new[i]=mutation(cenc[i])
            else:
                cenm_new[i]=cenm[i]
                cenc_new[i]=cenc[i]
                
        for i in range(m):
            for j in range(p):
                order_new[i][j]=cenm_new[i//m_p][(i%m_p)*p+j]
                order_new[i+m][j]=cenc_new[i//m_p][(i%m_p)*p+j]
                         
            
        fit_new,ordert_new=fitness(center,limit,limit_max,order_new)
        fit_list.append(fit)
        fit_new_list.append(fit_new)
        fit_best_list.append(fit_best)
        if fit_new>fit:
            order=order_new
            fit=fit_new
            if(fit_new>fit_best):
                order_best=order_new
                ordert_best=ordert_new
                fit_best=fit_new
                fit_list.append(fit_best)
                
        else:
            if random.random() < math.exp((fit_new -fit) / T):
                order=order_new
                fit=fit_new

        times=times+1
    T*=alpha
    #print("tempeture=",T)


print(order_best,fit_best)


#visualization
x=[0]*(2*n+3)
y=[0]*(2*n+3)
x[2*n]=center[0][0]
y[2*n]=center[0][1]
x[2*n+1]=center[1][0]
y[2*n+1]=center[1][1]
x[2*n+2]=center[2][0]
y[2*n+2]=center[2][1]

for i in range(n):
    x[i]=pm[i][0]
    y[i]=pm[i][1]
for i in range(n,2*n):
    x[i]=pc[i-n][0]
    y[i]=pc[i-n][1]
    

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'NSimSun,Times New Roman'
 
plt.plot(x, y, '*', label='merchant/customer', color='black')
plt.grid(alpha=0.5,linestyle='-.')
plt.xlabel('x')
plt.ylabel('y')



col=['blue','green','red','coral','purple','yellow']

for i in range(m):


    plt.plot([x[2*n+i//m_p],x[order_best[i][0]]],[y[2*n+i//m_p],y[order_best[i][0]]],color=col[i])
    plt.plot([x[2*n+i//m_p],x[order_best[i][p-1]]],[y[2*n+i//m_p],y[order_best[i][p-1]]],color=col[i])
 
    for j in range(p-1):
        plt.plot([x[order_best[i][j]],x[order_best[i][j+1]]],[y[order_best[i][j]],y[order_best[i][j+1]]],color=col[i]) 

    plt.plot([x[2*n+i//m_p],x[order_best[i+m][0]+n]],[y[2*n+i//m_p],y[order_best[i+m][0]+n]],color=col[i])
    plt.plot([x[2*n+i//m_p],x[order_best[i+m][p-1]+n]],[y[2*n+i//m_p],y[order_best[i+m][p-1]+n]],color=col[i])
    for j in range(p-1):
        plt.plot([x[order_best[i+m][j]+n],x[order_best[i+m][j+1]+n]],[y[order_best[i+m][j]+n],y[order_best[i+m][j+1]+n]],color=col[i]) 
    plt.plot([x[2*n],x[2*n+1]],[y[2*n],y[2*n+1]],color='black',linewidth=5)
    plt.plot([x[2*n],x[2*n+2]],[y[2*n],y[2*n+2]],color='black',linewidth=5)
    plt.plot([x[2*n+2],x[2*n+1]],[y[2*n+2],y[2*n+1]],color='black',linewidth=5)
        
plt.legend()
plt.show()

# show the time
print(np.mean(ordert_best))
