import matplotlib.pyplot as plt
import numpy as np
import time

DIST_MAX=10
station=np.array([[-12.856353,1.524696],[-5.68875,-2.168163],[27.818487,-12.002319],[-19.774317,20.724144],[18.884097,-16.146504],[-23.383704,6.219774],[24.125517,3.064488],[-11.09844,7.70784],[10,-15],[0,6]])
solve_list=[]
is_lightning = 0

zhongguancun=np.array([-5,9]) # 中关村商业中心
guoma=np.array([5.4,0.6]) # 国贸商业中心
xidan=np.array([-2,0.3]) # 西单商业中心
sanlitun=np.array([4.7,3]) # 三里屯商业中心
shuangjing=np.array([5.4,-1.5]) # 双井商业中心
shijingshan=np.array([-14.8,0]) # 石景山商业中心
cbd=np.array([6.8,0]) # 北京商务中心
shangdi=np.array([-8.6,14.9]) # 上地商业中心
donggaodi=np.array([1.4,-11]) # 东高地商业中心
panjiayuan=np.array([5.5,-3.5]) # 潘家园商业中心
dazhongshi=np.array([-4.6,6.5]) # 大钟寺商业中心
business_center_position=np.array([[-5,9],[5.4,0.6],[-2,0.3],[4.7,3],[5.4,-1.5],[-14.8,0],[6.8,0],[-8.6,14.9],[1.4,-11],[5.5,-3.5],[-4.6,6.5]])
business_center_name=["中关村","国贸","西单","三里屯","双井","石景山","北京","上地","东高地","潘家园","大钟寺"]

start = 0
end= 1


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
    global is_lightning
    is_lightning=1
    return close_end

def calculate_cost_lightning(dist_lightning):
    # 5公里以内，16元；5公里后每增加5km，加收10元；
    cost=16
    cycle=1
    while(1):
        if (dist_lightning-cycle*5)<=0:
            break
        cost +=10
        cycle +=1
    return cost

def calculate_time_lightning(dist_lightning):
    # 3公里45分钟，3公里到5公里增加15分钟，每超过5公里增加30分钟。
    time=45
    if dist_lightning<=3:
        return 45
    elif dist_lightning<=5:
        return 60
    time=60
    cycle=1
    while(1):
        if(dist_lightning-cycle*5)<=0:
            break
        time+=30
        cycle+=1
    return time

if __name__ == '__main__':
    f = open('info.txt',mode='w')
    for start in range(len(business_center_position)):
        end = start +1
        while( end<len(business_center_position) ):
            solve_list=[]
            is_lightning = 0
            plt.figure()
            plt.rcParams['font.sans-serif']=['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            # 初始化
            dist_trans=0
            dist_lightning=0
            cost_trans=0
            cost_lightning=0
            time_trans=0
            # 画散点
            draw_point()
            # 画端点
            plt.scatter([business_center_position[start][0],business_center_position[end][0]],[business_center_position[start][1],business_center_position[end][1]])
            plt.text(business_center_position[start][0]+1,business_center_position[start][1]+1,business_center_name[start])
            plt.text(business_center_position[end][0]-1,business_center_position[end][1]-1,business_center_name[end])
            # 画路径
            # 找最近点
            close_end=find_closed(business_center_position[end])
            close_start=find_closed(business_center_position[start])
            draw_link(business_center_position[end],close_end)
            draw_link(business_center_position[start],close_start)
            dist_trans += np.linalg.norm(business_center_position[end]-station[close_end])+np.linalg.norm(business_center_position[start]-station[close_start])
            dist_lightning=np.linalg.norm(business_center_position[start]-business_center_position[end])

            # 寻点存在solve_list中
            solve_list.append(close_start)
            solve(close_start,close_end)
            solve_list.append(close_end)
            for i in range(len(solve_list)-1):
                draw_line(solve_list[i],solve_list[i+1])
                dist_trans += np.linalg.norm(station[solve_list[i]]-station[solve_list[i+1]])
            
            # 价格
            cost_trans=5*(len(solve_list)+1)
            cost_lightning=calculate_cost_lightning(dist_lightning)

            # 时间
            # 时间=43min * 距离 /4km,
            time_trans=43*dist_trans/4.2
            time_lightning=calculate_time_lightning(dist_lightning)

            # 存入文件
            f.write(business_center_name[start]+'_to_'+business_center_name[end]+'\n')
            f.write("中转经过距离为:"+str(dist_trans)+"km\n")
            f.write("中转价格为:"+str(cost_trans)+"元\n")
            f.write("中转用时:"+str(time_trans)+"min\n")
            f.write("闪送直送距离为:"+str(dist_lightning)+"km\n")
            f.write("闪送价格为:"+str(cost_lightning)+"元\n")
            f.write("闪送用时:"+str(time_lightning)+"min\n")
            if(is_lightning==1):
                f.write("启用闪送\n")
            else:
                f.write("启用中转\n")
            f.write('**************************************\n')

            # print("中转经过距离为:",dist_trans,"km")
            # print("中转价格为:",cost_trans,"元")
            # print("中转用时",time_trans,"min")
            # print()
            # print("闪送直送距离为:",dist_lightning,"km")
            # print("闪送价格为:",cost_lightning,"元")
            # print("闪送用时",time_lightning,"min")
            # print()
            # if(is_lightning==1):
            #     print("启用闪送")
            # else:
            #     print("启用中转")
            # 画图
            plt.legend(loc='best')
            plt.savefig('./figure/'+business_center_name[start]+'_to_'+business_center_name[end]+'.png')
            # plt.show()
            # time.sleep(0.5)
            # plt.close()
            end +=1 
            plt.clf()
            plt.cla()
    f.close()