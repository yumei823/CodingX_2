#-*-coding:utf-8 -*-

#############################################
#              將所需函式庫加入             #
#############################################
import requests
from bs4 import BeautifulSoup
import os
import time
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import cm
import numpy as np

#############################################
#                讀取PTT網頁                 #
#############################################
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

#############################################
#          對PTT網頁進行資料擷取              #
#############################################
def get_data(dom):
    soup = BeautifulSoup(dom , 'html.parser')
    article = soup.find(id='main-content')
    
    return article

#############################################
#          		讀取文章網址            	 #
##################a##########################
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

#############################################
#    	讀取看板頁面(沒有加搜尋字眼時使用)     #
##################a##########################
def getNext(url):
    urls = get_web_page(url)
    soup = BeautifulSoup(urls, 'html.parser')
    div = soup.find_all('a','btn wide')
    for i in div:
        if i.getText() == '‹ 上頁':
            nextPage = 'https://www.ptt.cc' + i.get('href')
    return nextPage
    
#############################################
#          			畫圖				     #
##################a##########################
##################圓餅圖######################
def DrawPie(font, labels_list, percent_list, title):				#labels_list: 圓餅圖的字    #percent_list: 圓餅圖各項的比例
	labels, sizes = [], []											
	plt.title(title, fontproperties = font)
	for i in range(datazise):
		labels.append(str(labels_list[i]))
		sizes.append(str(percent_list[i]))
	colors = cm.rainbow(np.arange(len(sizes))/len(sizes))
	pictures,category_text,percent_text = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', shadow=True, startangle=140)
	for i in category_text:
		i.set_fontproperties(font)
	#plt.legend(loc = "upper right", prop = font)
	plt.axis('equal')

##################直方圖######################	
def DrawBar(font, sem_list, bar_list, title):						#sem_list: 直方圖的每條上的字   #bar_list: 直方圖的長度
	plt.title(title, fontproperties = font)
	y_pos = np.arange(1)
	plt.xticks(y_pos + .3/2, (''), fontproperties = font)
	for i in range(len(sem_list)):
		plt.bar(y_pos + 0.25*i , bar_list[i], 0.2, alpha=.5, label = sem_list[i])
	plt.legend(loc = "upper right", prop = font)
	
#############################################
#           主程式:進行資料分析              #
#############################################
if __name__ == '__main__':
    #1 = 'creditcard'
    #2 = 'Lifeismoney'
    #3 = '振興'
    #4 = '三倍'
    new_sum_sem_list = [0,0,0,0]
    datazise = eval(input("請輸入欲分析的詞彙個數  :  "))
    print('''省錢: Lifeismoney/CPBL: Elephants/籃球: NBA,
遊戲: LOL/Hate: HatePolitics/婚姻: marriage,
車車: car/資訊: MobileComm/工作: Tech_Job,
聊天: WomenTalk/心情: Boy-Girl/家庭: BabyMother,
硬體: PC_Shopping/娛樂: joke/主機: PlayStation,
韓國: KoreaStar/聯誼: AllTogether/理財: creditcard,
高雄: Kaohsiung/台南: Tainan/CPBL: Lions,
主機: NSwitch/CPBL:  Guardians/韓劇: KoreaDrama,
綜藝: KR_Entertain/手遊: PCReDive/資訊: CVS,
台中: TaichungBun/系統: iOS/美容: MakeUp''')
    Board = input("請輸入欲查詢看板 : ")
    semantic_list = []			#存放輸入的關鍵字
    for i in range(datazise):
        semantic_in = input("請輸入第"+str(i+1)+"個關鍵字  :  ")			#改變你想要找的關鍵字
        semantic_list.append(semantic_in)
    for q in range(0,4):
        KEY = 1#有沒有加入搜尋字眼 1:有 0:沒有
        if q == 0:
            # Board = 'creditcard'	    	#選取PTT看板	!!!!!!(凡是設有內容分級規定處理，即不能直接進入看板者，EX.八卦版...等會沒辦法爬)!!!!!
            Search = '振興'   		#加入搜尋特定字眼的文章 EX.在「省錢」/「理財」版找尋標題有含'振興券/卷'or'三倍券/卷'的文章
        elif q == 1:
            # Board = 'creditcard'
            Search = '三倍'
        elif q == 2:
            # Board = 'Lifeismoney'
            Search = '振興'
        elif q == 3:
            # Board = 'Lifeismoney'
            Search = '三倍'
        PTT_URL = 'https://www.ptt.cc/bbs/' if KEY == 1 else 'https://www.ptt.cc/bbs/' + Board + '/index.html'
        page_num = 10
        ############################################################
        '''
        datazise = eval(input("請輸入欲分析的詞彙個數  :  "))
        '''
        ############################################################
        #輸入關鍵字
        urls = []

        '''
        semantic_list = []			#存放輸入的關鍵字
        for i in range(datazise):
            semantic_in = input("請輸入第"+str(i+1)+"個關鍵字  :  ")			#改變你想要找的關鍵字
            semantic_list.append(semantic_in)
        '''
        ############################################################
        articles = []	#articles: ptt文章所有內容   #push_tags: 推噓文資訊
        for page in range(page_num):	#取得PTT頁面資訊
            url_key = PTT_URL + Board + '/search?page=' + str(page+1) + '&q=' + Search
            url = url_key if KEY == 1 else PTT_URL if page == 0 else getNext(PTT_URL)
            response = requests.get(url)
            urls = get_article_url(response.text)
        ############################################################
            for url in urls:
                print(url)
                text = get_web_page(url)
                article = get_data(text)
                articles.append(article)
                
        ############################################################
        #計算關鍵字出現次數，以及關鍵字出現的文章其推噓文數量
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


        ############################################################
        #將所有找尋到的字彙個數相加，計算總合
    sum_sem_list=new_sum_sem_list
    sum_all = sum(sum_sem_list)
    percent_list = []						#關鍵字佔比
        #計算單一詞彙佔全部字彙的百分比
    for i in range(datazise):
        if sum_all != 0:
            percent_list.append(round((sum_sem_list[i]*100)/sum_all,2))
        else:
            percent_list.append(0)

        ############################################################
        #準備繪圖
    pnb_list = []
    for i in range(datazise):
        bar_pnb = (sum_sem_list[i])
        pnb_list.append(bar_pnb)

    print('\r\r')
        ############################################################
    print("總搜尋字彙出現個數為 : ", sum_all)
    for i in range(datazise):
        print(semantic_list[i],"出現個數為:",sum_sem_list[i],"百分比為",percent_list[i],"%")

        #######################################
            #				將結果繪圖			  #
        #######################################
    myfont = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')							#字型檔，r'裡面放你的字型檔案路徑'
        #圓餅圖
    title1 = '關鍵字出現比例'
    plt.subplot(2,2,1)											#將圖表分割為2行2列，目前繪製的是第一格
    DrawPie(myfont, semantic_list, percent_list, title1)
        #長條圖
    title2 = '關鍵字出現總數'
    plt.subplot(2,2,2)											#將圖表分割為2行2列，目前繪製的是第二格
    DrawBar(myfont, semantic_list, pnb_list, title2)

    plt.show()
	#######################################
