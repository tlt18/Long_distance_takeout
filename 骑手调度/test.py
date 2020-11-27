import matplotlib.pyplot as plt
import numpy as np
# x=np.linspace(-1,1,50)
x=[-12.856353,-5.68875,27.818487,-19.774317,18.884097,-23.383704,24.125517,-11.09844]
y=[1.524696,-2.168163,-12.002319,20.724144,-16.146504,6.219774,3.064488,7.70784]
start=[0,-10]
end=[-21,20]

def draw_line(i,j,c=0):
    color=['r','b']
    plt.plot([x[i],x[j]],[y[i],y[j]],color=color[c],Linewidth=2)

def draw_point():
    plt.grid()
    plt.scatter(x,y,color=[1,0.9,0],label="Transfer Station")
    plt.scatter(0,0,s=200,marker='*',color='r',label="Centre")


if __name__ == '__main__':
    draw_point()
    # 画端点
    plt.scatter([start[0],end[0]],[start[1],end[1]])
    # 画路径
    plt.plot([end[0],x[3]],[end[1],y[3]],color='r',Linewidth=2)
    draw_line(3, 5)
    draw_line(5,0)
    draw_line(1,0)
    plt.plot([start[0],x[1]],[start[1],y[1]],color='r',Linewidth=2)
    plt.text(start[0]+1,start[1]+1,'start')
    plt.text(end[0]-2.,end[1]-2,'end')
    plt.legend(loc='best')
    plt.show()






