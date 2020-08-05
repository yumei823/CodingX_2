#-*-coding:utf-8 -*-

#
#
#
import requests
from bs4 import BeautifulSoup
import os
import time
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import cm
import numpy as np

#
#
#
def get_web_page(url):
    time.sleep(0.1)  
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

#
#
#
def get_data(dom):
    soup = BeautifulSoup(dom , 'html.parser')
    article = soup.find(id='main-content')
    push_tag = soup.find_all('span', 'push-tag')
    return article, push_tag

#
#
#
def get_article_url(text):
    url = []
    soup = BeautifulSoup(text, 'html.parser')
    divs = soup.find_all("div", "r-ent")
    for div in divs:
        try:
            href = div.find('a')['href']
            url.append('https://www.ptt.cc' + href)
        except:
            pass
    return url

#
# 
#
def getNext(url):
    urls = get_web_page(url)
    soup = BeautifulSoup(urls, 'html.parser')
    div = soup.find_all('a','btn wide')
    for i in div:
        if i.getText() == '‹ 上頁':
            nextPage = 'https://www.ptt.cc' + i.get('href')
    return nextPage
    

#
#
#
def DrawPie(font, labels_list, percent_list, title):	#labels_list: 圓餅圖的字    #percent_list: 圓餅圖各項的比例
	labels, sizes = [], []											
	plt.title(title, fontproperties = font)
	for i in range(datazise):
		labels.append(str(labels_list[i]))
		sizes.append(str(percent_list[i]))
	colors = cm.rainbow(np.arange(len(sizes))/len(sizes)) #在colormaps中選擇顏色為彩虹
	pictures,category_text,percent_text = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', shadow=True, startangle=140)
	for i in category_text:
		i.set_fontproperties(font)
#
	plt.axis('equal')

#	
def DrawBar(font, sem_list, bar_list, title):	#sem_list: 直方圖的每條上的字   #bar_list: 直方圖的長度
	plt.title(title, fontproperties = font)
	y_pos = np.arange(1)
	plt.xticks(y_pos + .3/2, (''), fontproperties = font)
	for i in range(len(sem_list)):
		plt.bar(y_pos + 0.25*i , bar_list[i], 0.2, alpha=.5, label = sem_list[i])
	plt.legend(loc = "upper right", prop = font)
	
#
#
#
if __name__ == '__main__':
    #1 = 'creditcard'
    #2 = 'Lifeismoney'
    #3 = '振興'
    #4 = '三倍'
    new_sum_sem_list = [0,0,0,0]
    datazise = eval(input("請輸入欲分析的詞彙個數  :  "))
    semantic_list = []			#存放輸入的關鍵字
    for i in range(datazise):
        semantic_in = input("請輸入第"+str(i+1)+"個關鍵字  :  ")
        semantic_list.append(semantic_in)
    for q in range(0,4):
        KEY = 1                         #是否加入搜尋字眼 1:有 0:沒有
        if q == 0:
            Board = 'creditcard'	#選取PTT看版
            Search = '振興'   		#加入搜尋特定字眼的文章 EX.在「省錢」/「理財」版找尋標題有含'振興券/卷'or'三倍券/卷'的文章
        elif q == 1:
            Board = 'creditcard'
            Search = '三倍'
        elif q == 2:
            Board = 'Lifeismoney'
            Search = '振興'
        elif q == 3:
            Board = 'Lifeismoney'
            Search = '三倍'
        PTT_URL = 'https://www.ptt.cc/bbs/' if KEY == 1 else 'https://www.ptt.cc/bbs/' + Board + '/index.html'
        page_num = 10
        #
        '''
        datazise = eval(input("請輸入欲分析的詞彙個數  :  "))
        '''
        #
        #
        urls = []

        '''
        semantic_list = []			#存放輸入的關鍵字
        for i in range(datazise):
            semantic_in = input("請輸入第"+str(i+1)+"個關鍵字  :  ")
            semantic_list.append(semantic_in)
        '''
        #
        articles, push_tags = [], []		
        for page in range(page_num):	#取得PTT頁面資訊
            url_key = PTT_URL + Board + '/search?page=' + str(page+1) + '&q=' + Search
            url = url_key if KEY == 1 else PTT_URL if page == 0 else getNext(PTT_URL)
            response = requests.get(url)
            urls = get_article_url(response.text)
        #
            for url in urls:
                print(url)
                text = get_web_page(url)
                article, push_tag = get_data(text)
                articles.append(article)
                push_tags.append(push_tag)
        #
        #
        sum_sem_list = []			#該關鍵字出現總數
        for i in range(datazise):
            sem_count = 0
            count = 0
            for index in articles:
                sem_count += str(index).count(semantic_list[i])
            sum_sem_list.append(sem_count)
        print(sum_sem_list)

        for i in range(0,4):
            new_sum_sem_list[i] = new_sum_sem_list[i] + sum_sem_list[i]
        print(new_sum_sem_list)


        #
        #計算所有關鍵字總合
    sum_sem_list=new_sum_sem_list
    sum_all = sum(sum_sem_list)
    percent_list = []				    #關鍵字佔比
        #計算單一關鍵字佔比
    for i in range(datazise):
        if sum_all != 0:
            percent_list.append(round((sum_sem_list[i]*100)/sum_all,2))
        else:
            percent_list.append(0)

#
#
    pnb_list = []
    for i in range(datazise):
        bar_pnb = (sum_sem_list[i])
        pnb_list.append(bar_pnb)

    print('\r\r')
#
    print("總搜尋字彙出現個數為 : ", sum_all)
    for i in range(datazise):
        print(semantic_list[i],"出現個數為:",sum_sem_list[i],"百分比為",percent_list[i],"%")

#
#
#
    myfont = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')	#字型檔，r'裡面放你的字型檔案路徑'
#
    title1 = '關鍵字出現比例'
    plt.subplot(2,2,1)					#將圖表分割為2行2列，目前繪製的是第一格
    DrawPie(myfont, semantic_list, percent_list, title1)
#
    title2 = '關鍵字出現總數'
    plt.subplot(2,2,2)					#將圖表分割為2行2列，目前繪製的是第二格
    DrawBar(myfont, semantic_list, pnb_list, title2)

    plt.show()
#
