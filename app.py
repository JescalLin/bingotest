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
import cv2

target = 0

app = Flask(__name__)
# 設置靜態文件緩存過期時間
app.send_file_max_age_default = timedelta(seconds=1)
 
@app.route('/stock', methods=['POST', 'GET'])  
def stock():
    if request.method == 'POST':
        target = str(request.form.get('target'))
        log = "開發中，敬請期待"
        return render_template('stock_ok.html',target=target,log=log,target=target)
    return render_template('stock.html')

@app.route('/bingo', methods=['POST', 'GET'])  
def bingo():
    if request.method == 'POST':
        target = int(request.form.get('target'))
        v_num = str(request.form.get('v_num'))
        b_date = str(request.form.get('b_date'))
        b_date_str = b_date.replace("-", "")
        url="https://lotto.auzonet.com/bingobingo/list_"+b_date_str+".html"

        all_num_array = list()
        time_date = list()
        num_data = list()
        res  = requests.get(url)
        soup = BeautifulSoup(res.text,'html.parser')
        table = soup.find('table', {'bordercolor': '#C0C0C0'})
        trs = table.find_all('tr', {'class': 'bingo_row'})
        tds = table.find_all('td', {'class': 'BPeriod'})
        for td in tds:
            time_date.append(td.text[-5:])
        for tr in trs:
            temp_row = list()
            temp_show_row = list()
            for div in tr.find_all('div'):
                temp_row.append(int(div.text))
            num_data.append(temp_row)

        if target ==0 or target > len(num_data):
            target = len(num_data)


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
            user_input = user_input +str(time_date[i])+" "+str(num_data[i])+"</br>"

        for k in range(5):
            plt.cla()
            plt.clf()
            cmap = colors.ListedColormap(['Blue','red'])
            plt.pcolor(all_num_array[k],cmap=cmap,edgecolors='k', linewidths=3)
            ax = plt.gca()
            ax.xaxis.set_ticks_position('top')
            ax.invert_yaxis() 

            for y in range(8):
                for x in range(10):
                    plt.text(x+0.5, y+0.5, str(y*10+x+1),
                            horizontalalignment='center',
                            verticalalignment='center',
                            color = "w", 
                            )
            
            plt.savefig("static/images/p_"+str(k)+".jpg")

        img0 = cv2.imread("static/images/p_0.jpg")
        img1 = cv2.imread("static/images/p_1.jpg")
        img2 = cv2.imread("static/images/p_2.jpg")
        img3 = cv2.imread("static/images/p_3.jpg")
        img4 = cv2.imread("static/images/p_4.jpg")
        v_img = cv2.vconcat([img0,img1,img2,img3,img4])
        cv2.imwrite("static/images/test2.jpg",v_img)

        #組間分析
        A_spilt_num = 0
        B_spilt_num = 0
        C_spilt_num = 0
        D_spilt_num = 0
        A_score = 0
        B_score = 0
        C_score = 0
        D_score = 0
        for k in range(target):
            A_spilt_num_s = 0
            B_spilt_num_s = 0
            C_spilt_num_s = 0
            D_spilt_num_s = 0
            for i in range(80):
                if i in num_data[k] and i<20:
                    A_spilt_num = A_spilt_num +1
                    A_spilt_num_s = A_spilt_num_s +1
                if i in num_data[k] and i>=20 and i<40:
                    B_spilt_num = B_spilt_num +1 
                    B_spilt_num_s = B_spilt_num_s +1         
                if i in num_data[k] and i>=41 and i<60:
                    C_spilt_num = C_spilt_num +1
                    C_spilt_num_s = C_spilt_num_s +1  
                if i in num_data[k] and i>=61 and i<80:
                    D_spilt_num = D_spilt_num +1 
                    D_spilt_num_s = D_spilt_num_s +1  

            temp_array = [A_spilt_num_s,B_spilt_num_s,C_spilt_num_s,D_spilt_num_s]
            temp_array= sorted(temp_array,reverse=True)

            for i in range(4):
                if A_spilt_num_s == temp_array[i]:
                    A_score = A_score + 3-i
                if B_spilt_num_s == temp_array[i]:
                    B_score = B_score + 3-i
                if C_spilt_num_s == temp_array[i]:
                    C_score = C_score + 3-i
                if D_spilt_num_s == temp_array[i]:
                    D_score = D_score + 3-i

        spilt_num = "綜合</br>A組(1~20):"+str(A_spilt_num)+"</br>"+"B組(21~40):"+str(B_spilt_num)+"</br>"+"C組(41~60):"+str(C_spilt_num)+"</br>"+"D組(61~80):"+str(D_spilt_num)+"</br>"
        spilt_num = "</br>"+spilt_num+"</br>分次</br>A組(1~20):"+str(A_score)+"</br>"+"B組(21~40):"+str(B_score)+"</br>"+"C組(41~60):"+str(C_score)+"</br>"+"D組(61~80):"+str(D_score)+"</br>"

        #虛擬下注
        v_num_a = v_num.split(' ')
        v_num_a = list(map(int, v_num_a))
        v_text = ""
        v_text = "下注成本:"+str(25*target)+"</br>"
        v_money = 0
        for k in range(target):
            bingo_result = 0
            v_tempmoney = 0
            for i in range(3):
                if v_num_a[i] in num_data[k]:
                    bingo_result = bingo_result + 1
            if bingo_result == 2:
                v_money = v_money + 50
                v_tempmoney = 50
            if bingo_result == 3:
                v_money = v_money + 500
                v_tempmoney = 500
            v_text = v_text + str(time_date[k])+" 中"+str(bingo_result)+"星 賺"+str(v_tempmoney)+"元</br> "
        v_final_money =  "總損益:"+ str(v_money-(25*target))+"元"


        #連續未開
        temp_array = []
        for k in range(len(num_data)):
            b_target = [0]*80
            for i in range(80):
                ball_num = i+1
                if ball_num in num_data[k]:
                    b_target[i] = 1
                else:
                    b_target[i] = 0
            temp_array.append(b_target)

        b_count = [0]*80

        for k in range(80):
            for i in range(len(temp_array)):
                if temp_array[i][k]==0:
                    b_count[k]=b_count[k]+1
                else:
                    break

        noopen_num = ""
        for i in range(80):
            noopen_num = noopen_num + str(i+1)+":"+str(b_count[i])+"</br>"

        

        # #開獎表格

        # all_num_array_1D=[]
        # for k in range(target):
        #     num_array = [0]*80
        #     for i in range(80):
        #         if (i+1) in num_data[k]:
        #             num_array[i]=1
        #     all_num_array_1D.append(num_array)


        # plt.figure(figsize=(32,10))
        # plt.cla()
        # plt.clf()
        # cmap = colors.ListedColormap(['Blue','red'])
        # plt.pcolor(all_num_array_1D,cmap=cmap,edgecolors='k', linewidths=3)

        # ax = plt.gca()
        # ax.xaxis.set_ticks_position('top')
        # ax.set_aspect('equal')
        # ax.xaxis.set_major_locator(plt.MultipleLocator(1))
        # ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        # ax.invert_yaxis() 

        # # 去除白框
        # plt.margins(0,0)
        # plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
        # # 保存图片，cmap为调整配色方案
        # plt.savefig("static/images/numb.jpg")


                    
        


        return render_template('bingo_ok.html',target=target,userinput=user_input,connum2=str(sorted_x2),connum3=str(sorted_x3),spilt_num=str(spilt_num),v_text=v_text,v_num=v_num,v_final_money=v_final_money,b_date=b_date,noopen_num=noopen_num)
 
    return render_template('bingo.html')
 
 
if __name__ == '__main__':
    app.run()