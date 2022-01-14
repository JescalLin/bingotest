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


#"https://lotto.auzonet.com/biglotto/list_2021_all.html"
#"https://lotto.auzonet.com/biglotto/list_2022_all.html"



time_date_2021 = list()
num_data_2021 = list()
time_date_2022 = list()
num_data_2022 = list()
time_date = list()
num_data = list()
target = 10

url="https://lotto.auzonet.com/biglotto/list_2021_all.html"
res  = requests.get(url)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,'html.parser')
table = soup.find_all('table', {'class': 'history_view_table'})
for i in range(len(table)):
    li = table[i].find('li', {'class': 'ball_blue'})
    balls = li.find_all('a', {'class': 'history_ball_link'})
    sp_ball = table[i].find('td', attrs={'style':'color:#005aff; font-size:48px; font-weight:bolder;'})
    td = table[i].find('td', {'rowspan': '2','align':"center"})
    time = td.find('span', attrs={'style':'font-size:18px; color:#fb4202; font-weight:bold;'})
    num_data_2021.append([int(balls[0].encode_contents()),int(balls[1].encode_contents()),int(balls[2].encode_contents()),int(balls[3].encode_contents()),int(balls[4].encode_contents()),int(balls[5].encode_contents()),int(balls[0].encode_contents()),int(sp_ball.encode_contents())])
    time_date_2021.append(str(time.encode_contents().decode("utf-8")))

num_data_2021 = num_data_2021[::-1]
time_date_2021 = time_date_2021[::-1]



url="https://lotto.auzonet.com/biglotto/list_2022_all.html"
res  = requests.get(url)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,'html.parser')
table = soup.find_all('table', {'class': 'history_view_table'})
for i in range(len(table)):
    li = table[i].find('li', {'class': 'ball_blue'})
    balls = li.find_all('a', {'class': 'history_ball_link'})
    sp_ball = table[i].find('td', attrs={'style':'color:#005aff; font-size:48px; font-weight:bolder;'})
    td = table[i].find('td', {'rowspan': '2','align':"center"})
    time = td.find('span', attrs={'style':'font-size:18px; color:#fb4202; font-weight:bold;'})
    num_data_2022.append([int(balls[0].encode_contents()),int(balls[1].encode_contents()),int(balls[2].encode_contents()),int(balls[3].encode_contents()),int(balls[4].encode_contents()),int(balls[5].encode_contents()),int(balls[0].encode_contents()),int(sp_ball.encode_contents())])
    time_date_2022.append(str(time.encode_contents().decode("utf-8")))

num_data_2022 = num_data_2022[::-1]
time_date_2022 = time_date_2022[::-1]

num_data = num_data_2021 + num_data_2022
time_date = time_date_2021 + time_date_2022

num_data = num_data[::-1]
time_date = time_date[::-1]

num_data = num_data[0:target]
time_date = time_date[0:target]



