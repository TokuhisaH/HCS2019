import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime as dt
import csv
import math

#ファイル読み込み
file_name = 'matuken_music' 
data = pd.read_csv(file_name + '.csv',header=None)

db = list(map(float, data[0]))

#分割数
anaCnt = 30

#分割する数
n = 18000

#配列宣言
db_list = [db[i:i+n] for i in range(0,len(db),n)]


db_except = [[]]
count = [[]]

db_list_except0 = []

index =0

#ゼロを排除し、その前後2つの0を排除
for db_target in db_list:
    #db_list_except.append([i for i in db_target if i != 0])
    db_list_except0.append(list(filter(lambda x: x !=0, db_target)))
    if len(db_list_except0[index])>4:
        del db_list_except0[index][:2]
        del db_list_except0[index][-2:]  
    index +=1

db_list_log=[]
log=[]
for i in range(len(db_list_except0)):
    log.append([math.log(j,math.e) for j in db_list_except0[i]])   
    db_list_log.append(log[i]) 



db_list_0 =[]
for i in range(len(db_list_except0)):
    db_list_0.append(n-len(db_list_except0[i]))

for i in range(len(db_list_0)):
    db_list_0[i]=db_list_0[i]/100


# print(db_list_0)


# 平均
def calculate_mean(data):
    s = sum(data)
    N = len(data)
    mean =s/N

    return mean

#平均からの偏差を求める
def find_difference(data):
    mean = calculate_mean(data)
    diff = []

    for num in data:
        diff.append(num-mean)
    return diff

def calculate_variance(data):
    diff = find_difference(data)
    #差の２乗を求める
    squared_diff = []
    for d in diff:
        squared_diff.append(d**2)

    #分散を求める
    sum_squared_diff = sum(squared_diff)
    variance = sum_squared_diff/len(data)
    return variance

calc_list =[]
variance_list = []
std_list = []


if __name__ == '__main__':
    for i in range(len(db_list_except0)):
        if len(db_list_except0[i]) !=0:
            #平均
            calc_list.append(calculate_mean(db_list_except0[i]))
            #分散
            variance_list.append(calculate_variance(db_list_except0[i]))
            # #標準偏差
            std_list.append(variance_list[i]**0.5)
            # #変動係数
            # cov = std_start/calculate_mean(db_start_except0)
    
#    print(len(std_list))

with open('data.csv', 'a',newline="") as f:
    writer = csv.writer(f)
    writer.writerow(std_list)

 with open('silent.csv', 'a') as f:
     writer = csv.writer(f)
     writer.writerow(db_list_0)

    print(file_name)
    print('平均')
    print(calc_list)
    print('標準偏差')
    print(std_list)
    print('無音区間')
    print(db_list_0)

#グラフ表示　

# plt.subplot(2,1,1)
# plt.title('average')
# plt.xlim(xmax=15)
# plt.plot(calc_list)
# plt.subplot(2,1,2)
# plt.xlim(xmax=15)
# plt.title('standard deviation')
# plt.plot(std_list)
# plt.subplot(3,1,3)

#plt.show()