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


#27
num_data=[
[3, 5, 17, 19, 21, 23, 24, 29, 30, 42, 45, 53, 56, 58, 62, 66, 67, 68, 75, 79]
,[1, 3, 4, 5, 13, 14, 19, 23, 26, 32, 38, 39, 40, 45, 53, 59, 60, 61, 65, 67]
,[7, 8, 10, 16, 21, 25, 30, 32, 33, 34, 39, 43, 49, 53, 58, 60, 70, 72, 78, 80]
,[3, 4, 6, 9, 12, 13, 21, 22, 31, 36, 37, 38, 46, 49, 52, 58, 65, 67, 70, 78]
,[2, 9, 14, 15, 21, 23, 32, 34, 36, 37, 38, 40, 41, 48, 57, 60, 64, 65, 67, 70]
,[2, 3, 6, 9, 10, 14, 15, 16, 17, 18, 21, 24, 29, 31, 37, 44, 51, 60, 72, 74]
,[6, 7, 10, 15, 18, 25, 26, 27, 33, 34, 43, 47, 51, 59, 62, 64, 65, 67, 72, 73]
,[1, 2, 4, 7, 10, 13, 16, 17, 22, 33, 37, 41, 42, 45, 46, 50, 61, 64, 69, 70]
,[4, 6, 9, 15, 17, 20, 24, 27, 31, 32, 38, 41, 47, 50, 52, 53, 54, 55, 58, 59]
,[1, 3, 11, 14, 16, 17, 20, 33, 34, 37, 43, 49, 50, 54, 57, 58, 64, 65, 74, 78]]

all_num_array_1D=[]
for k in range(len(num_data)):
    num_array = [0]*80
    for i in range(80):
        if (i+1) in num_data[k]:
            num_array[i]=1
    all_num_array_1D.append(num_array)


plt.figure(figsize=(32,10))
plt.cla()
plt.clf()
cmap = colors.ListedColormap(['Blue','red'])
plt.pcolor(all_num_array_1D,cmap=cmap,edgecolors='k', linewidths=3)

ax = plt.gca()
ax.xaxis.set_ticks_position('top')
ax.set_aspect('equal')
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.invert_yaxis() 

# 去除白框
plt.margins(0,0)
plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
# 保存图片，cmap为调整配色方案
plt.savefig("static/images/numb.jpg")


#[1,7,0,1,0,.....]

# temp_array = []
# for k in range(len(num_data)):
#     b_target = [0]*80
#     for i in range(80):
#         ball_num = i+1
#         if ball_num in num_data[k]:
#             b_target[i] = 1
#         else:
#             b_target[i] = 0
#     temp_array.append(b_target)


# b_count = [0]*80

# for k in range(80):
#     for i in range(len(temp_array)):
#         if temp_array[i][k]==0:
#             b_count[k]=b_count[k]+1
#         else:
#             break

# noopen_b = ""
# for i in range(80):
#     noopen_b = noopen_b + str(i+1)+":"+str(b_count[i])+"\n"


# print(noopen_b)


