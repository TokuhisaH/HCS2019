import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime as dt
import csv

#ファイル読み込み
file_name = 'echigo_music' 
data = pd.read_csv(file_name + '.csv',header=None)

db = list(map(float, data[0]))

min_vol=32 #音量を無効にする閾値

#分割数
anaCnt = 15

#分割する数
n = 6000

#配列宣言
db_list = [db[i:i+n] for i in range(0,len(db),n)]


db_except = [[]]
count = [[]]

db_list_except0 = []
db_list_0 =[]
df=pd.DataFrame()
for db_target in db_list:
    #db_list_except.append([i for i in db_target if i != 0])
    db_list_except0.append(list(filter(lambda x: x >=min_vol, db_target)))


#無音区間の算出
db=[]
db_list_0=[]
db_length_list=[] #無音区間の長さno
db_max=[] #最長の無音区間のリスト
silent_list=[] #無音区間をカウントする
for i in range(len(db_list)):
    silent_cnt=0
    db.clear()
    db_list_0.clear()
    db_length_list.clear()
    def func1(lst, value):
        return [j for j, x in enumerate(lst) if x > value]

    a = func1(db_list[i],min_vol)

    for j in range(len(db_list[i])):
        if j not in a:
            db.append(j)
            if j == len(db_list[i])-1:
                db_list_0.append(db.copy()) 
                db_length_list.append(len(db.copy())) 
                if len(db.copy())>=100 and len(db.copy())<=200:
                    silent_cnt +=1
        else:
            if not db:
                pass
            else:
                db_list_0.append(db.copy())
                db_length_list.append(len(db.copy()))
                if len(db.copy())>=100 and len(db.copy())<=200:
                    silent_cnt +=1
                db.clear()
    db_max.append(max(db_length_list))

    if silent_cnt !=0:
        silent_list.append(silent_cnt)
    else:
        silent_list.append(0)


# print(db_max)







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

#データの出力
with open('data.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(calc_list)

#無音区間の長さの最長を出力
# with open('silent_max.csv', 'a') as f:
#     writer = csv.writer(f)
#     writer.writerow(db_max)

#1秒以上の無音区間の回数を取得
with open('silent_cnt.csv', 'a',newline="") as f:
    writer = csv.writer(f)
    writer.writerow(silent_list)

    print(file_name)
    print('平均')
    print(calc_list)
    print('標準偏差')
    print(std_list)
    print('無音回数')
    print(silent_list)

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