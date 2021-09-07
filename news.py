from PIL import Image,ImageFont,ImageDraw
import cn2an as cn2an
from time import time, localtime, strftime
import requests
import json,os
# import matplotlib.pyplot as plt

from zhdate import ZhDate


# 天行数据的key
tx_key = os.environ['KEY']



#背景

def bgimg():
    bg_size = (1080, 2300)
    bg_small=(980,330)
    img = Image.new("RGBA",bg_size,(245,245,245))
    draw = ImageDraw.Draw(img)

    w,h = bg_small
    #左上角坐标
    x,y=(50,50)
    #圆角直径
    r=30
    '''Rounds''' 
    draw.ellipse((x,y,x+r,y+r),fill=(166,207,166))    
    draw.ellipse((x+w-r,y,x+w,y+r),fill=(166,207,166))    
    draw.ellipse((x,y+h-r,x+r,y+h),fill=(166,207,166))    
    draw.ellipse((x+w-r,y+h-r,x+w,y+h),fill=(166,207,166))
    '''rec.s'''    
    draw.rectangle((x+r/2,y, x+w-(r/2), y+h),fill=(166,207,166))    
    draw.rectangle((x,y+r/2, x+w, y+h-(r/2)),fill=(166,207,166))

    '''画线'''
    draw.line((50, 400,1030,400) ,(66,66,65), width=5)  #线的起点和终点，线宽
    draw.line((50, 600,1030,600) ,(189,192,200), width=3)

    # draw.line((0,0,0,2300),(255, 227, 21), width=5)
    # draw.line((1080,0,1080,2300),(255, 227, 21), width=5)
    # draw.line((0,0,0,2300),(255, 227, 21), width=5)
    # draw.line((0,0,0,2300),(255, 227, 21), width=5)

    draw_text(draw)
   
    # img.show()

    # return img ,draw
    return img 


def draw_text(draw):

    #加载字体文件
    fontpath = "./font/SIMYOU.TTF"
    fontpath1 = "./font/GB2312.ttf"
    font = ImageFont.truetype(fontpath1,80, encoding="utf-8")
    #在图片上添加文字
    #fill用来设置绘制文字的颜色,(R,G,B)
    today = int(strftime("%w"))
    if 0 == today:
        today = '星期日'
    else:
        today = '星期' + cn2an.an2cn(today)
    font = ImageFont.truetype(fontpath1,80, encoding="utf-8")
    draw.text((430, 65), today, font=font, fill=(255, 255, 255))
    font_small = ImageFont.truetype(fontpath1, 35)
    draw.text((50, 450), "农历", font=font_small, fill=(0, 0, 0))
    draw.text((50, 500),nonli(), font=font_small, fill=(0, 0, 0))
    draw.text((910, 450), strftime("%Y年", localtime(time())), font=font_small, fill=(0, 0, 0))
    draw.text((870, 500), strftime("%m月%d日", localtime(time())), font=font_small, fill=(0, 0, 0))



    font_sentence = ImageFont.truetype(fontpath, 25)
    draw.text((220,280),verse(),font=font_sentence)


    font_news = ImageFont.truetype(fontpath, 35)
    draw.text((110, 650), historyList(), font=font_news, fill=(0, 0, 0))

    draw.line((50, 960,1030,960) ,(189,192,200), width=3)

    draw.text((110, 1020), news(), font=font_news, fill=(0, 0, 0))
    font_red = ImageFont.truetype(fontpath, 40)

    




    return draw



# 农历
def nonli():
    day = str(ZhDate.today())
    day =day[7:] 
    return day


# 每日简报
def news():
    req_url = 'http://api.tianapi.com/bulletin/index?key=' + tx_key
    response = requests.get(req_url)
    loads = json.loads(response.text)
    news_list = loads.get('newslist')
    news = ''
    for index in range(len(news_list)):
        if index > 14:
            return news
        title = news_list[index].get('title')
        if len(title) > 25:
            title = title[:25] + '\n\n' + title[25:]
        news += str(index + 1) + '、' + title + '\n\n'
        
        
    return news

# 名言
def verse():
    req_url = 'http://api.tianapi.com/txapi/lzmy/index?key=' + tx_key
    response = requests.get(req_url)
    loads = json.loads(response.text)
    verse_list = loads.get('newslist')
    source = verse_list[0].get('source')
    saying = verse_list[0].get('saying')
    verse_str = '【微语】 ' + saying
    resp_verse = verse_str
    if len(verse_str) > 22:
        resp_verse = verse_str[:26] + '\n' + verse_str[26:]
    return resp_verse


def historyList():
    date =requests.get('https://news.topurl.cn/api').json()
    list=date['data']['historyList']
    historytitle = ''
    for index in range(len(list)):
        title = list[index].get('event')
    # print(title)
        if len(title) > 25:
            title = title[:25] + '\n\n' + title[25:]
        historytitle +=  title + '\n\n'
    # print(historytitle)
    return historytitle











def save_img(img):
    # img.show()

    img_path = os.path.join('.', 'outpic', 'png_paste.png')
    img.save(img_path)
    print('保存成功 at {}'.format(img_path))
    # img.save("./draw_img.png")






if __name__ == '__main__':
    # draw_text(bgimg())
    save_img(bgimg())