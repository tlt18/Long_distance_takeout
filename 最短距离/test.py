import matplotlib.pyplot as plt
import numpy as np

DIST_MAX=10
station=np.array([[-12.856353,1.524696],[-5.68875,-2.168163],[27.818487,-12.002319],[-19.774317,20.724144],[18.884097,-16.146504],[-23.383704,6.219774],[24.125517,3.064488],[-11.09844,7.70784],[10,-15],[0,-10]])
solve_list=[]
start=np.array([0,-10])
# start=np.array([20,-15])
end=np.array([-21,20])

# 画出连接ij两个站点的线段
def draw_line(i,j,c=0):
    color=['r','b']
    plt.plot([station[i][0],station[j][0]],[station[i][1],station[j][1]],Color=color[c],Linewidth=2)

# 画出散点
def draw_point():
    plt.grid()
    for point in station:
        plt.scatter(point[0],point[1],color=[1,0.9,0])
        plt.text(point[0]+1,point[1]+1,(np.argwhere(station==point)[0][0]))
    plt.scatter(0,0,s=200,marker='*',color='r',label="Centre")

# 画出端点和点i的连线
def draw_link(endpoint,i,c=0):
    color=['r','b']
    plt.plot([station[i][0],endpoint[0]],[station[i][1],endpoint[1]],Color=color[c],Linewidth=2)

# 对于一个端点返回最近的点的索引
def find_closed(endpoint):
    dist=[]
    for point in station:
        dist.append(np.linalg.norm(endpoint-point)) 
    return dist.index(min(dist))

def solve(now,close_end):
    next = find_next(now,close_end)
    if(next==close_end):
        return
    solve_list.append(next)
    solve(next,close_end)

def find_next(now,close_end):
    if(np.linalg.norm( station[now]-station[close_end] ) < DIST_MAX):
        return close_end
    dot_list=[]
    for point in station:
        dot=np.dot(station[close_end]-station[now],point-station[now] )
        dot_list.append(dot)
    # 对内积序列进行小到大排序，argsort返回索引
    close_index_list=np.argsort(dot_list)
    for index in close_index_list[::-1]:
        if( np.linalg.norm(station[now]-station [index] ) < DIST_MAX and dot_list[index]>0 ):
            return index
    # 所有投影都不满足，直接走向最终点
    return close_end

if __name__ == '__main__':
    # 画散点
    draw_point()
    # 画端点
    plt.scatter([start[0],end[0]],[start[1],end[1]])
    plt.text(start[0]+1,start[1]+1,'start')
    plt.text(end[0]-1,end[1]-1,'end')
    # 画路径
    # 找最近点
    close_end=find_closed(end)
    close_start=find_closed(start)
    draw_link(end,close_end)
    draw_link(start,close_start)
    # 寻点存在solve_list中
    solve_list.append(close_start)
    solve(close_start,close_end)
    solve_list.append(close_end)
    print(solve_list)
    for i in range(len(solve_list)-1):
        draw_line(solve_list[i],solve_list[i+1])

    # 画图
    plt.legend(loc='best')
    plt.show()