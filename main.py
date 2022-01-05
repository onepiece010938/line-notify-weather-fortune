#-*- coding: utf-8 -*-
#基本功能測試
import requests
import json
import time
import codecs
import sys
from bs4 import BeautifulSoup
import re
from zhconv import convert
import random 
import matplotlib.pyplot as plt
import pandas as pd
import os

# plt.rcParams['font.sans-serif']='Microsoft-JhengHei'
from matplotlib.font_manager import *  #定義自定義字體，文件名從1.b查看系統中文字體中來
plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
myfont = FontProperties(fname='/home/ubuntu/Desktop/Linebot/華康娃娃體.TTF') #改用自ㄝ
font_for_symbol_path = "/home/ubuntu/.local/lib/python3.8/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans-Bold.ttf"
font_for_symbol = FontProperties(fname=font_for_symbol_path)



sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
'''
imageFile and imgurl 只能則一使用
'''
def send_notify(token, msg, filepath=None, imgurl=None,stickerPackageId=None, stickerId=None):
    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + token
     }
    if stickerPackageId and stickerId:
        payload['stickerPackageId'] = stickerPackageId
        payload['stickerId'] = stickerId

    if filepath:
        attachment = {'imageFile': open(filepath, 'rb')}
        # print(attachment)
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload, files=attachment)
    elif imgurl:
        payload['imageThumbnail'] = imgurl
        payload['imageFullsize'] = imgurl
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    else:
        # print("attachment")
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code, r.text

def get_weather():
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-093"
    params = {
        "Authorization": "-------",
        "locationId": "F-D0047-069", #新北 台北市61
        "locationName":"新莊區"
    }
    element_name=[]
    # print(type(params))
    response = requests.get(url, params=params)
    # print(response.status_code)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)
        # print(type(data))
        location = data["records"]["locations"][0]["locationsName"]
        # print(location)
        location_detail = data["records"]["locations"][0]["location"][0]["locationName"]
        # print(location_detail)
        weather_elements = data["records"]["locations"][0]["location"][0]["weatherElement"]
        for i in range(0,len(weather_elements)):
            www = weather_elements[i]["elementName"]
            element_name.append(www)
        # print("共%d個天氣因子" %len(element_name))
        # print(element_name)
        # print(weather_elements[3])
        
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        # print(location)
        # print(start_time)
        # print(end_time)
        # print(weather_state)
        # print(rain_prob)
        # print(min_tem)
        # print(comfort)
        # print(max_tem)

    else:
        print("Can't get data!")
    


def get_today_temperature_01():
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-093"
    params = {
        "Authorization": "-----",
        "locationId": "F-D0047-069", #新北 台北市61
        "locationName":"新莊區",
        "timeFrom":"" ,#Format: 2021-11-09T17:19:54
        "timeTo":"",
        "elementName":"T"
    }
    params2 = {
        "Authorization": "-----",,
        "locationId": "F-D0047-069", #新北 台北市61
        "locationName":"新莊區",
        "timeFrom":"" ,#Format: 2021-11-09T17:19:54
        "timeTo":"",
        "elementName":"AT" #體感溫度
    }
    params3 = {
        "Authorization": "-----",,
        "locationId": "F-D0047-069", #新北 台北市61
        "locationName":"新莊區",
        "timeFrom":"" ,#Format: 2021-11-09T17:19:54
        "timeTo":"",
        "elementName":"WeatherDescription" #
    }
    localtime = time.localtime()
    # time_now = time.strftime("%Y-%m-%dT%H:%M:%S", localtime)
    time_get_date = time.strftime("%Y-%m-%dT06:00:00", localtime)
    params["timeFrom"] = time_get_date
    # 要抓前7筆到隔天00:00:00
    print(time_get_date)
    element_name=[]
    weather_elements_list=[]
    # print(type(params))
    response = requests.get(url, params=params)
    response2 = requests.get(url, params=params2)
    response3 = requests.get(url, params=params3)
    # print(response.status_code)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)
        data2 = json.loads(response2.text)
        data3 = json.loads(response3.text)
        # print(type(data))
        location = data["records"]["locations"][0]["locationsName"]
        # print(location)
        location_detail = data["records"]["locations"][0]["location"][0]["locationName"]
        # print(location_detail)
        message = '\n來看看 大小寶家 今天的天氣呦\n' # %0D%0A  換行
        message = message + "==="+location +" "+location_detail+ "==="+"\n"
        weather_elements = data["records"]["locations"][0]["location"][0]["weatherElement"]
        weather_elements2 = data2["records"]["locations"][0]["location"][0]["weatherElement"]
        weather_elements3 = data3["records"]["locations"][0]["location"][0]["weatherElement"]
        for i in range(0,len(weather_elements)):
            www = weather_elements[i]["elementName"]
            element_name.append(www)
        for i in range(0,3): #要抓前7筆到隔天00:00:00 小寶只要x[0124]
            weather_elements_value = weather_elements[0]["time"][i]
            weather_elements_value2 = weather_elements2[0]["time"][i]
            weather_elements_value3 = weather_elements3[0]["time"][i]
            # print(weather_elements_value3)
            message = message + "時間: "+ weather_elements_value["dataTime"]+"\n"
            message = message + "溫度:"+ weather_elements_value["elementValue"][0]["value"]+" 度"+"  體感溫度:"+weather_elements_value2["elementValue"][0]["value"]+" 度\n"
            value = weather_elements_value3["elementValue"][0]["value"]
            rain_index = value.find("降雨機率")
            rain_index2 = value.find("%")
            rain_value = value[rain_index:rain_index2+1]
            # print(rain_value)
            message = message + rain_value+"\n"
        weather_elements_value = weather_elements[0]["time"][4]
        weather_elements_value2 = weather_elements2[0]["time"][4]
        weather_elements_value3 = weather_elements3[0]["time"][4]
        message = message + "時間: "+ weather_elements_value["dataTime"]+"\n"
        message = message + "溫度:"+ weather_elements_value["elementValue"][0]["value"]+" 度"+"  體感溫度:"+weather_elements_value2["elementValue"][0]["value"]+" 度\n"
        value = weather_elements_value3["elementValue"][0]["value"]
        rain_index = value.find("降雨機率")
        rain_index2 = value.find("%")
        rain_value = value[rain_index:rain_index2+1]
        # print(rain_value)
        message = message + rain_value+"\n"
        #     weather_elements_list.append(weather_elements_value)
        
        # message = message + "時間: "+ weather_elements_list[0]["dataTime"]+"\n"
        # message = message + "溫度:"+ weather_elements_list[0]["elementValue"][0]["value"]+" 度\n"
        # print(weather_elements_list)
           
        return message
        # print("共%d個天氣因子" %len(element_name))
        # print(element_name)
        # print(weather_elements[3])
    else:
        print("Can't get data!")
        return response.status_code

def get_today_temperature_02():
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-093"
    params = {
        "Authorization": "-----",,
        "locationId": "F-D0047-061", #新北 台北市61
        "locationName":"大安區",
        "timeFrom":"" ,#Format: 2021-11-09T17:19:54
        "timeTo":"",
        "elementName":"T"
    }
    params2 = {
        "Authorization": "-----",,
        "locationId": "F-D0047-061", #新北 台北市61
        "locationName":"大安區",
        "timeFrom":"" ,#Format: 2021-11-09T17:19:54
        "timeTo":"",
        "elementName":"AT" #體感溫度
    }
    params3 = {
        "Authorization": "-----",,
        "locationId": "F-D0047-069", #新北 台北市61
        "locationName":"新莊區",
        "timeFrom":"" ,#Format: 2021-11-09T17:19:54
        "timeTo":"",
        "elementName":"WeatherDescription" #
    }
    localtime = time.localtime()
    # time_now = time.strftime("%Y-%m-%dT%H:%M:%S", localtime)
    time_get_date = time.strftime("%Y-%m-%dT06:00:00", localtime)
    params["timeFrom"] = time_get_date
    # 要抓前7筆到隔天00:00:00
    # print(time_get_date)
    element_name=[]
    weather_elements_list=[]
    # print(type(params))
    response = requests.get(url, params=params)
    response2 = requests.get(url, params=params2)
    response3 = requests.get(url, params=params3)
    # print(response.status_code)

    if response.status_code == 200:
        data = json.loads(response.text)
        data2 = json.loads(response2.text)
        data3 = json.loads(response3.text)
        location = data["records"]["locations"][0]["locationsName"]
        location_detail = data["records"]["locations"][0]["location"][0]["locationName"]
        message = '\n來看看 小寶家 今天的天氣呦\n' # %0D%0A  換行
        message = message + "==="+location +" "+location_detail+ "==="+"\n"
        weather_elements = data["records"]["locations"][0]["location"][0]["weatherElement"]
        weather_elements2 = data2["records"]["locations"][0]["location"][0]["weatherElement"]
        weather_elements3 = data3["records"]["locations"][0]["location"][0]["weatherElement"]
        for i in range(0,len(weather_elements)):
            www = weather_elements[i]["elementName"]
            element_name.append(www)
        for i in range(0,3): #要抓前7筆到隔天00:00:00
            weather_elements_value = weather_elements[0]["time"][i]
            weather_elements_value2 = weather_elements2[0]["time"][i]
            weather_elements_value3 = weather_elements3[0]["time"][i]
            # print(weather_elements_value)
            message = message + "時間: "+ weather_elements_value["dataTime"]+"\n"
            message = message + "溫度:"+ weather_elements_value["elementValue"][0]["value"]+" 度"+"  體感溫度:"+weather_elements_value2["elementValue"][0]["value"]+" 度\n"
            value = weather_elements_value3["elementValue"][0]["value"]
            rain_index = value.find("降雨機率")
            rain_index2 = value.find("%")
            rain_value = value[rain_index:rain_index2+1]
            # print(rain_value)
            message = message + rain_value+"\n"
        weather_elements_value = weather_elements[0]["time"][4]
        weather_elements_value2 = weather_elements2[0]["time"][4]
        weather_elements_value3 = weather_elements3[0]["time"][4]
        message = message + "時間: "+ weather_elements_value["dataTime"]+"\n"
        message = message + "溫度:"+ weather_elements_value["elementValue"][0]["value"]+" 度"+"  體感溫度:"+weather_elements_value2["elementValue"][0]["value"]+" 度\n"
        value = weather_elements_value3["elementValue"][0]["value"]
        rain_index = value.find("降雨機率")
        rain_index2 = value.find("%")
        rain_value = value[rain_index:rain_index2+1]
        message = message + rain_value+"\n"
        return message

    else:
        print("Can't get data!")
        return response.status_code




def zodiacSigns(ans_data):
    # 星座轉換字典
    zodiacSigns_convent = {
    '1':'Aries',
    '2':'Taurus',
    '3':'Gemini',
    '4':'Cancer',
    '5':'Leo',
    '6':'Virgo',
    '7':'Libra',
    '8':'Scorpio',
    '9':'Sagittarius',
    '10':'Capricorn',
    '11':'Aquarius',
    '12':'Pisces'
    }

    # 題問說明
    question_description = "[1]牡羊座 [2]金牛座 [3]雙子座 [4]巨蟹座 [5]獅子座 [6]處女座 [7]天秤座 [8]天蠍座 [9]射手座 [10]摩羯座 [11]水瓶座 [12]雙魚座，請選擇星座(僅能填數字):"

    # ans_data='1'
    # 網址內容為唐綺陽每日星座運勢
    url = 'https://www.daily-zodiac.com/mobile/zodiac/' + zodiacSigns_convent[ans_data]
    response = requests.get(url)

    # 設定讀取編碼(預設 UTF-8)
    response.encoding = 'UTF-8'

    # 檢查 HTTP 回應碼是否為 200
    if response.status_code == requests.codes.ok:
        sp = BeautifulSoup(response.text, 'html.parser')
        zodiacSigns_name = sp.select(".middle .name .name")[0].text # 星座名稱
        zodiacSigns_date = sp.select(".middle .name .date")[0].text # 星座日期
        today_date = sp.select(".today li")[1].text # 今日日期
        today_horoscope_weather = sp.select(".today .weather")[0].text #今日心情
        
        # 移除字串開頭的空格 str.lstrip()
        # 移除字串末尾的空格 str.rstrip()
        today_horoscope = sp.select("section article")[0].text.lstrip()
        
    #   印出結果
        # print('[%s %s 今日運勢]' %(zodiacSigns_name, zodiacSigns_date))
        # print('今日日期:%s' %(today_date))
        # print('今日心情:%s' %(today_horoscope_weather))
        # print('今日評語:\n%s' %(today_horoscope))
        msg = '[%s %s 今日運勢]' %(zodiacSigns_name, zodiacSigns_date)
        msg =msg + '\n今日日期:%s' %(today_date)
        msg =msg+ "\n今日心情:%s" %(today_horoscope_weather)
        msg =msg+'\n今日評語:\n%s' %(today_horoscope)
        return msg

def daily_soup():
    url ="http://wufazhuce.com"
    r = requests.get(url)
    r.encoding = 'utf-8'
    res = r.text
    list = re.findall(r'<a href="http://wufazhuce.com/one/([\w\W]*?)a>',res)
    # for sentence in list:
    #     print(sentence)

    one = "\n".join(re.findall(r'">([\w\W]*?)</',list[1]))
    # print(list[1])
    '''
    3374">我的心里有一颗种子，~~~机会，也给自己一个机会。</
    '''
    # print('one sentence = ', one)
    msg = convert(one,'zh-tw')
    msg = "\n ====今天的心靈雞湯==== \n"+msg
    '''
    3374"><img class="fp-one-imagen" src="http://image.wufazhuce.com/FpgOKdaT4EwfyM7zv-_HcdjLmcqz" alt="" /></
    '''
    # print(list[0])
    img_url = "\n".join(re.findall(r'src="([\w\W]*?)"',list[0]))
    # print(img_url)
    # print(msg)
    return msg,img_url


def good_mood_fliter(string_bao): 
    # 紀錄輸入星座名
    get_zodiac = string_bao[0:46]
    # print(get_zodiac)
    if string_bao.find("今日心情:陰")!=-1 or string_bao.find("今日心情:打雷")!=-1 or string_bao.find("今日心情:雨")!=-1:
        # print(string_bao.find("今日心情:陰") , string_bao.find("今日心情:打雷") , string_bao.find("今日心情:雨"))
        good_mood = ""
        for i in range (1,12+1):
            if i ==11:
                continue
            tmp_result = zodiacSigns(str(i))
            if tmp_result.find("今日心情:陰")!=-1 or tmp_result.find("今日心情:打雷")!=-1 or tmp_result.find("今日心情:雨")!=-1:
                continue
            else:
                good_mood = tmp_result
                # 要把偷抓出來別的星座名 替換成 輸入的星座名 還有今日日期 星座所屬日期
                good_mood = good_mood.replace(good_mood[0:46],get_zodiac[0:46])
                break
        
        if good_mood== "":
            good_mood = string_bao[0:46]+"\n今日心情:晴 \n今日評語:\n今天是當快樂小寶的一天, 凡事不要想太多, 只管開心就好。感情方面只要對另一半越好，對方就會越愛妳。今天大寶是妳的貴人，要珍惜與他互動的機會,他可以幫妳解決任何煩惱。幸運色是大寶色。"  
        
        # 紀念日 通通都是快樂小寶
        localtime = time.localtime()
        if localtime.tm_mday == 3:
            good_mood = string_bao[0:46]+"\n今日心情:晴 \n今日評語:\n今天是當快樂小寶的一天, 凡事不要想太多, 只管開心就好。感情方面只要對另一半越好，對方就會越愛妳。今天大寶是妳的貴人，要珍惜與他互動的機會,他可以幫妳解決任何煩惱。幸運色是大寶色。"  

        return good_mood
    else:
        return string_bao

def get_sticker_id(): # get random sticker
    All_PackageId=[446,789,6326,6632,8525]
    All_stickerId=[[1988,2027],[10855,10894],[11087920,11087943],[11825374,11825397],[16581290,16581313]]
    rd_index = random.randint(0, 4)
    PackageId = All_PackageId[rd_index]
    stickerId = random.randint(All_stickerId[rd_index][0],All_stickerId[rd_index][1])
    return PackageId,stickerId
    
def save_as_img(temperature_message): 
    # ⁂ ☂ ☁ ☀ ☃ ☪ ❄ 
    str2 = temperature_message.split('\n')
    area = str2[2].split(' ')
    area = area[1].split('===')
    area = area[0]


    str_time = str2[3]
    str_time = str_time.split(' ')
    str_date = str_time[1]
    r1_str_time = str_time[2]
    # print(r1_str_time) #12:00:00
    # print(str_date) #2021-12-21

    r1_t_all = str2[4] #溫度:20 度  體感溫度:23 度
    r1_t_all = r1_t_all.split(':')
    r1_t = r1_t_all[1].split(' ')[0] #20
    r1_at = r1_t_all[2].split(' ')[0] #23
    r1_pr = str2[5] #降雨機率 90%
    r1_pr = r1_pr.split(' ')[1] #90%
    # print(r1_pr) #90%
    # print(r1_t) #20
    # print(r1_at) #23
    int_r1_pr = int(r1_pr.split("%")[0])
    if int_r1_pr >= 50:
        r1_pic = "☂"
    elif int_r1_pr>=10 and int_r1_pr <50:
        r1_pic = "☁"
    else:
        r1_pic = "☀"
    int_r1_at = int(r1_at)
    if int_r1_at < 20:
        r1_pic += " + ☃"

    
    r2_t_all = str2[7] 
    r2_t_all = r2_t_all.split(':')
    r2_t = r2_t_all[1].split(' ')[0]
    r2_at = r2_t_all[2].split(' ')[0]
    r2_pr = str2[8] 
    r2_pr = r2_pr.split(' ')[1]
    r2_str_time = str2[6].split(' ')[2]
    int_r2_pr = int(r2_pr.split("%")[0])
    if int_r2_pr >= 50:
        r2_pic = "☂"
    elif int_r2_pr>=10 and int_r2_pr <50:
        r2_pic = "☁"
    else:
        r2_pic = "☀"
    int_r2_at = int(r2_at)
    if int_r2_at < 20:
        r2_pic += " + ☃"

    r3_t_all = str2[10] 
    r3_t_all = r3_t_all.split(':')
    r3_t = r3_t_all[1].split(' ')[0]
    r3_at = r3_t_all[2].split(' ')[0]
    r3_pr = str2[11] 
    r3_pr = r3_pr.split(' ')[1]
    r3_str_time = str2[9].split(' ')[2]
    int_r3_pr = int(r3_pr.split("%")[0])
    if int_r3_pr >= 50:
        r3_pic = "☂"
    elif int_r3_pr>=10 and int_r3_pr <50:
        r3_pic = "☁"
    else:
        r3_pic = "☀"
    int_r3_at = int(r3_at)
    if int_r3_at < 20:
        r3_pic += " + ☃"

    r4_t_all = str2[13] 
    r4_t_all = r4_t_all.split(':')
    r4_t = r4_t_all[1].split(' ')[0]
    r4_at = r4_t_all[2].split(' ')[0]
    r4_pr = str2[14] 
    r4_pr = r4_pr.split(' ')[1]
    r4_str_time = str2[12].split(' ')[2]
    int_r4_pr = int(r4_pr.split("%")[0])
    if int_r4_pr >= 50:
        r4_pic = "☂"
    elif int_r4_pr>=10 and int_r4_pr <50:
        r4_pic = "☁"
    else:
        r4_pic = "☪"
    int_r4_at = int(r4_at)
    if int_r4_at < 20:
        r4_pic += " + ☃"
 


    plt.figure()
    fig, ax = plt.subplots() 
    # ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    data=[[r1_pic,r2_pic,r3_pic,r4_pic],
        [r1_t,r2_t,r3_t,r4_t],
        [r1_at,r2_at,r3_at,r4_at],
        [r1_pr,r2_pr,r3_pr,r4_pr]]
    column_labels=[r1_str_time, r2_str_time, r3_str_time,r4_str_time]
    row_index=["天氣","溫度","體感溫度","降雨機率"]
    df=pd.DataFrame(data,columns=column_labels,index=row_index)
    # print(df)
    
    ax.axis('tight')
    ax.axis('off')
    my_table = pd.plotting.table(ax, df, loc='center',cellLoc="center") #將mytable投射到ax上，且放置於ax的中間

    # 要改圖示字體 不然會顯示不出來  找字體參照 找unicode符號存在哪個tff中.txt
    # my_table.get_celld()[(0, 0)].get_text().set_text(tmp)
    my_table.get_celld()[(1, 0)].set_text_props(fontproperties=font_for_symbol)
    my_table.get_celld()[(1, 1)].set_text_props(fontproperties=font_for_symbol)
    my_table.get_celld()[(1, 2)].set_text_props(fontproperties=font_for_symbol)
    my_table.get_celld()[(1, 3)].set_text_props(fontproperties=font_for_symbol)
    # print(my_table.get_celld()[(1, 1)].get_text())
    # print(my_table.get_celld()[(1, 2)].get_text())
    # ⁂ ☂ ☁ ☀ ☃ ☪ ❄

    # 調整表格大小跟字體大小
    my_table.scale(1, 2)
    my_table.auto_set_font_size(False)
    my_table.set_fontsize(20)

    

    # my_table = my_table.fontproperties=myfont
    # my_table.setfontstyle='italic'


    ax.set_title(str2[1]+"\n"+str2[2]+"\n"+str_date,fontweight ="bold",fontproperties=myfont,fontsize=24,y = 0.755 ,x = 0.4)
    save_path = "/home/ubuntu/Desktop/Linebot/"+area+".png"
    plt.savefig(save_path, bbox_inches='tight', dpi=300, transparent=True)
    plt.cla()
    plt.close('all')
if __name__ == "__main__":






    token = '--'
    # 今日溫度通知
    temperature_message_01 = get_today_temperature_01()
    save_as_img(temperature_message_01)
    time.sleep(1)
    temperature_message_02 = get_today_temperature_02()
    save_as_img(temperature_message_02)

    
    
    if isinstance(temperature_message_01, int):
        print("ERROR:",temperature_message_01)
    else:
        PackageId,stickerId = get_sticker_id()
        time.sleep(1)
        filepath='/home/ubuntu/Desktop/Linebot/新莊區.png'
        while os.path.isfile(filepath)!=True:
            print("繪圖失敗")
            save_as_img(temperature_message_01)
        else:
            print("新莊區.png 繪圖成功")
        # save_as_img(temperature_message_01)
        # save_as_img(temperature_message_01)
        #  傳送通知
        # status_code,txt= send_notify(token=token, msg= temperature_message_01, stickerPackageId=PackageId, stickerId=stickerId)
        status_code,txt= send_notify(token=token,msg="大小寶們ㄉ家",filepath='/home/ubuntu/Desktop/Linebot/新莊區.png')
        print (status_code)
        print (txt)
        i = 0
        while status_code != 200 or "新莊區" not in temperature_message_01:
            break
            i +=1
            #  傳送通知
            # status_code,_ = send_notify(token=token, msg= get_today_temperature_01(), stickerPackageId=PackageId, stickerId=stickerId)
            save_as_img(temperature_message_01)
            time.sleep(5)
            status_code,txt= send_notify(token=token,msg="大小寶們ㄉ家",filepath='/home/ubuntu/Desktop/Linebot/新莊區.png')
            print (status_code,"i: ",i)
            if i>= 100:
                break
        print (status_code,"i: ",i)
    if isinstance(temperature_message_02, int):
        print("ERROR:",temperature_message_02)
    else:
        PackageId,stickerId = get_sticker_id()
        filepath='/home/ubuntu/Desktop/Linebot/大安區.png'
        while os.path.isfile(filepath)!=True:
            print("繪圖失敗")
            save_as_img(temperature_message_02)
        else:
            print("大安區.png 繪圖成功")
        #  傳送通知
        status_code,txt= send_notify(token=token,msg="我的小可愛寶的家",filepath='/home/ubuntu/Desktop/Linebot/大安區.png') 
        print (status_code)
        print (txt)
        i = 0
        while status_code != 200 or "大安區" not in temperature_message_02:
            break
            i +=1
            #  傳送通知
            # status_code,_ = send_notify(token=token, msg= get_today_temperature_02(), stickerPackageId=PackageId, stickerId=stickerId)
            save_as_img(temperature_message_02)
            time.sleep(5)
            status_code,txt= send_notify(token=token,msg="我的小可愛寶的家",filepath='/home/ubuntu/Desktop/Linebot/大安區.png') 
            print (status_code,"i: ",i)
            if i>= 100:
                break  
        print (status_code,"i: ",i)
    

    img = "https://www.7car.tw/uploads/article/966/62966/7car-201912160957-3.jpg"
    # 今日星座運勢通知
    # "[1]牡羊座 [2]金牛座 [3]雙子座 [4]巨蟹座 [5]獅子座 [6]處女座 [7]天秤座 [8]天蠍座 [9]射手座 [10]摩羯座 [11]水瓶座 [12]雙魚座
    little_bao_sign = zodiacSigns("1")
    big_bao_sign = zodiacSigns("11")

    little_bao_sign= good_mood_fliter(little_bao_sign)
    # big_bao_sign = good_mood_fliter(big_bao_sign)

    little_bao_sign = "\n來看看 小寶 今天ㄉ星座運勢\n"+little_bao_sign
    big_bao_sign = "\n來看看 大寶 今天ㄉ星座運勢\n"+big_bao_sign
    

    # print(little_bao_sign)
    # print(big_bao_sign)
    PackageId,stickerId = get_sticker_id()
    #  傳送通知 小寶星座
    status_code,txt=send_notify(token=token, msg= little_bao_sign)
    print (status_code)
    print (txt)
    i =0
    while status_code!=200:
        status_code,txt=send_notify(token=token, msg= little_bao_sign)
        if i>= 100:
            break
    print (status_code,"i: ",i)
    print (txt)
    #  傳送通知 大寶星座
    status_code,txt=send_notify(token=token, msg= big_bao_sign, stickerPackageId=PackageId, stickerId=stickerId)
    i =0
    while status_code!=200:
        status_code,txt=send_notify(token=token, msg= big_bao_sign, stickerPackageId=PackageId, stickerId=stickerId)
        if i>= 100:
            break
    print (status_code,"i: ",i)
    print (status_code)
    print (txt)
    # 每日一句 one雞湯
    one_soup,img_url = daily_soup()
    #  傳送通知 雞湯
    send_notify(token=token, msg= one_soup,imgurl=img_url)
    # get_weather()


#   lineNotifyMessage(token, message)
#   lineNotifyMessage(token, message, img)
  # Test line notify
#   send_notify(token=token, msg='測試', filepath='/Linebot/01.png')

#   send_notify(token=token, msg='測試22222', imgurl=img , stickerPackageId=789, stickerId=10856)
  

