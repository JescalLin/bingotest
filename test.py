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

lingu_fee_o = 0
lingu_fee = 0

targer = 17.9
fee = 0.001425
log = ""
temp_min = 100000
temp_index = 0
for i in range(1000):
    input_v = i+1
    input_count = math.ceil(1000/input_v)
    lingu_fee_o = input_v*fee*targer
    lingu_fee = math.floor(lingu_fee_o)
    if(lingu_fee<2):
        lingu_fee = 1
    if lingu_fee*input_count > temp_min:
        pass
    else:
        temp_min = lingu_fee*input_count
        temp_index = input_v
    log = log + " "+str(input_v)+" "+str(input_count)+" "+str(lingu_fee)+" "+str(lingu_fee*input_count)+"\n"

print("最佳零股:"+str(temp_index)+" 手續費:"+str(temp_min))

print(log)