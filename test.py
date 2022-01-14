from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt 
from matplotlib import colors
from matplotlib.pyplot import MultipleLocator
import seaborn as sns
from collections import Counter
from itertools import combinations
import cv2
import math
import pandas as pd
import csv



# url="https://lotto.auzonet.com/bingobingo/list_20220113.html"
# all_num_array = list()
# time_date = list()
# num_data = list()
# res  = requests.get(url)
# soup = BeautifulSoup(res.text,'html.parser')
# table = soup.find('table', {'bordercolor': '#C0C0C0'})
# trs = table.find_all('tr', {'class': 'bingo_row'})
# tds = table.find_all('td', {'class': 'BPeriod'})
# for td in tds:
#     time_date.append(td.text[-5:])
# for tr in trs:
#     temp_row = list()
#     temp_show_row = list()
#     for div in tr.find_all('div'):
#         temp_row.append(int(div.text))
#     num_data.append(temp_row)

# print(num_data)






time_date = list()
num_data = list()
target = 10
with open('./data/大樂透_2021.csv', newline='' ,encoding="utf-8") as csvfile:

  # 讀取 CSV 檔內容，將每一列轉成一個 dictionary
  rows = csv.DictReader(csvfile)
  # 以迴圈輸出指定欄位
  for row in rows:
    time_date.append(row['期別'])
    num_data.append([int(row['獎號1']),int(row['獎號2']),int(row['獎號3']),int(row['獎號4']),int(row['獎號5']),int(row['獎號6']),int(row['特別號'])])


#二球熱門組合
array2_all = []
array2_temp = []
for i in range(target):
    array2_temp = list(combinations(num_data[i], 2))
    for j in range(len(array2_temp)):
        array2_all.append(array2_temp[j])
d2 = Counter(array2_all)
sorted_x2 = sorted(d2.items(), key=lambda x2: x2[1], reverse=True)
#三球熱門組合
array3_all = []
array3_temp = []
for i in range(target):
    array3_temp = list(combinations(num_data[i], 3))
    for j in range(len(array3_temp)):
        array3_all.append(array3_temp[j])
d3 = Counter(array3_all)
sorted_x3 = sorted(d3.items(), key=lambda x3: x3[1], reverse=True)
print(str(sorted_x2))
print(str(sorted_x3))


#連續未開
temp_array = []
for k in range(target):
    b_target = [0]*49
    for i in range(49):
        ball_num = i+1
        if ball_num in num_data[k]:
            b_target[i] = 1
        else:
            b_target[i] = 0
    temp_array.append(b_target)
b_count = [0]*49
for k in range(49):
    for i in range(len(temp_array)):
        if temp_array[i][k]==0:
            b_count[k]=b_count[k]+1
        else:
            break
noopen_num = ""
for i in range(49):
    noopen_num = noopen_num + str(i+1)+":"+str(b_count[i])+"</br>"
tmp = max(b_count)
index = b_count.index(tmp)
index = str(index+1)
noopen_num = noopen_num+"最多期未開號碼"+str(index)+"</br>"

print(noopen_num)