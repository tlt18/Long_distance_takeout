import math
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib as mpl

#n is the number of order
n=12
#m is the number of food delivery man
m=6
#t is the crossover point
mid=m//2
T_init=1000
T_min=0.1
alpha=0.9
loop_times=1000
v=500/3
t_pre=10



# center=[1612.5,750.0]

center=[3225.0, 1500.0]

#pc is the position of customers,pm is the position of merchants
pc=[0]*n
pm=[0]*n
order=[0]*m
order1=[0]*m
order2=[0]*m

#test data

limit=[10,10,10,20,20,20,30,30,30,40,50,50]
limit_max=[30,40,40,35,35,35,50,50,60,60,70,70]
"""
pm=[[725.0,2200.0],[1575.0,2587.5],[1062.5,875.0],[1650.0,1512.5],[637.5,1012.5],[1425.0,1887.5],[1650.0,1512.5],[2962.5,1150.0],[625.0,2562.5],[2137.5,1987.5],[2187.5,625.0],[912.5,687.5]]
pc=[[1925.0,1062.5],[1787.5,412.5],[737.5,425.0],[1837.5,2362.5],[1262.5,2075.5],[1687.5,1650.0],[737.5,1537.5],[1562.5,575.0],[1262.5,2075.0],[2712.5,1737.5],[2825.0,2425.0],[2625.0,2262.5]]
"""
pm=[[1450.0,4400.0],[3150.0,5175.0],[2125.0,1750.0],[3300.0,3025.0],[1275.0,2025.0],[2850.0,3775.0],[3300.0,3025.0],[5925.0,2300.0],[1250.0,5125.0],[4275.0,3975.0],[4375.0,1250.0],[1825.0,1375.0]]
pc=[[3850.0,2125.0],[3575.0,825.0],[1475.0,850.0],[3675.0,4725.0],[2525.0,4151.0],[3375.0,3300.0],[1475.0,3075.0],[3125.0,1150.0],[2525.0,4150.0],[5425.0,3475.0],[5650.0,4850.0],[5250.0,4525.0]]


#calculate Manhattan distance
def distance(a,b):
    e=abs(a[0]-b[0])+abs(a[1]-b[1])
    return e

#shuffle序列元素随机排序,相当于a序列顺序不变,返回的a_new是a的重新排列
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

#ab前半段进行交换
def crossover(a,b):
    d=len(a)
    e=d//2
    c=[0]*e
    for i in range(e):
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
    dist=[0]*m
    t_m=[0]*m
    for i in range(m):
        length=2
        dist[i]=[0]*(length*2+1)
        dist[i][0]=distance(center,pm[order[i][0]])
        dist[i][length*2]=distance(center,pc[order[i][length*2-1]])
        dist[i][length]=distance(pm[order[i][length-1]],pc[order[i][length]])
        for j in range(1,length):
            dist[i][j]=distance(pm[order[i][j-1]],pm[order[i][j]])
        for j in range(length+1,2*length):
            dist[i][j]=distance(pc[order[i][j-1]],pc[order[i][j]])
        t=[0]*length
        for j in range(length+1):
            t[0]=t[0]+dist[i][j]/v
        t[0]=t[0]+t_pre
        for j in range(1,length):
            t[j]=t[j-1]+dist[i][j+length+1]/v
        for j in range(length):
            sum=sum+satisfaction(limit[order[i][length+j]],limit_max[order[i][length+j]],t[j])
        t_m[i]=np.mean(t)

    return sum,t_m
        
        
                  
#initialization        
p=n//m
q=n%m
a=[0]*n
for i in range(n):
    a[i]=i
random.shuffle(a)

for i in range(m-1):
    order[i]=[0]*p*2
    order1[i]=[0]*p
    order2[i]=[0]*p
    for j in range(p):
        order1[i][j]=a[i*p+j]
    
order[m-1]=[0]*(n-m*p+p)*2
order1[m-1]=[0]*(n-m*p+p)
order2[m-1]=[0]*(n-m*p+p)
for j in range(p):
    order1[m-1][j]=a[(m-1)*p+j]
for i in range(m):
    l=len(order1[i])
    for j in range(l):
        order2[i][j]=order1[i][j]
for i in range(m):
    random.shuffle(order1[i])
    order[i]=order1[i]+order2[i]

#main program
T=T_init
fit_best_list=list()
fit_list=list()
fit_new_list=list()
t_m=[0]*m
t_mbest=[0]*m
order_best=order
fit_best,t_mbest=fitness(center,limit,limit_max,order_best)
fit_list.append(fit_best)
while T>T_min:
    times=0
    while(times<loop_times):
        fit,t_m=fitness(center,limit,limit_max,order)
        temp1=random.random()
        temp2=random.random()
        temp3=random.randint(0,m-1)
        temp4=random.randint(0,m-1)
        #初始化新序列
        order1_new=order1
        order2_new=order2
        if temp1>0.3:
            #pass
            #这里本来不就相等吗？
            if temp2>0.5:
                #某骑手new和原序列交换
                order1_new[temp3]=mutation(order1[temp3])
            else:
                #某骑手new和原序列交换
                order2_new[temp3]=mutation(order2[temp3])
        else:
            #序列1两个骑手前半段订单交换
            crossover(order1_new[temp3],order1_new[temp4])
            #两种可能序列交换
            order2_new[temp3]=mutation(order1_new[temp3])
            order2_new[temp4]=mutation(order1_new[temp4])
        order_new=[0]*m
        for i in range(m):
            order_new[i]=order1_new[i]+order2_new[i]
        #这里只更新了fit_new
        fit_new,t_mnew=fitness(center,limit,limit_max,order_new)

        fit_list.append(fit)
        fit_new_list.append(fit_new)
        fit_best_list.append(fit_best)
        if fit_new>fit:
            for i in range(m):
                l=len(order1[i])
                for j in range(l):
                    order1_new[i][j]=order1[i][j]
                    order2_new[i][j]=order2[i][j]
            order=order_new
            #更新fit
            fit=fit_new
            if(fit_new>fit_best):
                order_best=order_new
                t_mbest=t_mnew
                fit_best=fit_new
                fit_list.append(fit_best)
                
        else:
            if random.random() < math.exp((fit_new -fit) / T):
                for i in range(m):
                    l=len(order1[i])
                    for j in range(l):
                        order1_new[i][j]=order1[i][j]
                        order2_new[i][j]=order2[i][j]
                order=order_new
                fit=fit_new
            else:
                for i in range(m):
                    l=len(order1_new[i])
                    for j in range(l):
                        order1[i][j]=order1_new[i][j]
                        order2[i][j]=order2_new[i][j]
        times=times+1
    T*=alpha
    #print("tempeture=",T)







print(order_best,fit_best)


#visualization
x=[0]*(2*n+1)
y=[0]*(2*n+1)
x[2*n]=center[0]
y[2*n]=center[1]
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

col=['blue','green','red','coral','black','purple']

for i in range(m):
    length=int(len(order[i])/2)
    plt.plot([x[2*n],x[order[i][0]]],[y[2*n],y[order[i][0]]],color=col[i])
    plt.plot([x[2*n],x[order[i][2*length-1]+n]],[y[2*n],y[order[i][2*length-1]+n]],color=col[i])
    plt.plot([x[order[i][length-1]],x[order[i][length]+n]],[y[order[i][length-1]],y[order[i][length]+n]],color=col[i])
    for j in range(length-1):
        plt.plot([x[order[i][j]],x[order[i][j+1]]],[y[order[i][j]],y[order[i][j+1]]],color=col[i]) 
    for j in range(length,2*length-1):
        plt.plot([x[order[i][j]+n],x[order[i][j+1]+n]],[y[order[i][j]+n],y[order[i][j+1]+n]],color=col[i]) 

print(t_mbest)
        
plt.legend()
plt.show()

# show the time

