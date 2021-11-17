from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt 
from matplotlib import colors
import seaborn as sns
from collections import Counter
from itertools import combinations

target = 0

app = Flask(__name__)
# 設置靜態文件緩存過期時間
app.send_file_max_age_default = timedelta(seconds=1)
 
@app.route('/bingo', methods=['POST', 'GET'])  
def bingo():
    if request.method == 'POST':
        target = int(request.form.get('target'))
        res  = requests.get("https://www.taiwanlottery.com.tw/lotto/bingobingo/drawing.aspx")
        soup = BeautifulSoup(res.text,'html.parser')
        table = soup.find('table', attrs={'class':'tableFull'})
        table = table.find("tr")
        raw_data = []
        num_data = []
        rows = table.find_all('tr')[3:]
        all_num_array = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data = [ele for ele in cols if ele] # Get rid of empty values
            raw_data.append(data)
            data_num = data[1].replace("  ", " ")
            data_num =list(map(int, data_num.strip().split()))  
            num_data.append(data_num)  
        if target ==0:
            target = len(num_data)


        #一球熱門號碼
        array1_all = []
        for i in range(target):
            for num in range(20):
                array1_all.append(num_data[i][num])
        d1 = Counter(array1_all)
        sorted_x1 = sorted(d1.items(), key=lambda x1: x1[1], reverse=True)
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
        #熱門號碼圖
        for k in range(len(num_data)):
            num_array = np.zeros((8, 10))
            for i in range(8):
                for j in range(10):
                    checknum=i*10+j+1
                    if checknum in num_data[k]:
                        num_array[i][j]=1
            all_num_array.append(num_array)

        test_array= np.zeros((8, 10))
        for i in range(target):
            test_array = test_array+all_num_array[i]
        plt.figure(figsize=(6,6))
        ax = sns.heatmap(test_array , linewidth = 3 , cmap = 'OrRd', xticklabels =False, yticklabels=False)
        for y in range(8):
            for x in range(10):
                plt.text(x + 0.5, y + 0.5, str(y*10+x+1),
                        horizontalalignment='center',
                        verticalalignment='center',
                        color = "b", 
                        )
        plt.xticks(np.arange(0,10,step=1))
        plt.yticks(np.arange(0,8,step=1))
        plt.savefig("static/images/test1.jpg")
        user_input = ""
        for i in range(target):
            user_input = user_input +str(num_data[i])+"</br>"

        cmap = colors.ListedColormap(['Blue','red'])
        plt.rcParams["figure.figsize"] = [20, 20]
        for i in range(5):
            plt.subplot(5, 1, i+1)
            for y in range(8):
                for x in range(10):
                    plt.text(x, y, str(y*10+x+1),
                            horizontalalignment='center',
                            verticalalignment='center',
                            color = "w", 
                            )
            plt.imshow(all_num_array[i],cmap=cmap)
        plt.savefig("static/images/test2.jpg")


        return render_template('bingo_ok.html',target=target,userinput=user_input,connum1=str(sorted_x1),connum2=str(sorted_x2),connum3=str(sorted_x3))
 
    return render_template('bingo.html')
 
 
if __name__ == '__main__':
    #app.run(host='10.9.31.18', port=8000 ,debug=True)
    app.run()