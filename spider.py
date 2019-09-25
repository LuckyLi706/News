from urllib import request
from news import NewsBean
from bs4 import BeautifulSoup
import time


class Spider:
    baseurl = "http://www.mnw.cn/news/"

    # 获取html的内容
    def __gethtml(self, type):
        r = request.urlopen(Spider.baseurl + type)  # 向这个地址发送http请求
        htmls = r.read()  # 读取获取的html内容
        htmls = str(htmls, encoding='utf-8')  # 使用utf-8进行编码
        return htmls

    # 分析html,分析所需要的数据
    @staticmethod
    def __analysis(htmls):
        soup = BeautifulSoup(
            htmls,  # HTML文档字符串
            'html.parser',  # HTML解析器
            from_encoding='utf-8'  # HTML文档的编码
        )
        all = soup.find_all('div', attrs={'class': 'item noimg', 'class': 'item'})
        news_list = []
        for i in range(all.__len__() - 1, -1, -1):

            url = all[i].find('a').attrs['href']
            content = all[i].find('p').text
            str1 = all[i].find('span').text
            # print(str1)
            time1 = str1.split()[0] + ' ' + str1.split()[1]
            timeArray = time.strptime(time1, "%Y-%m-%d %H:%M")
            timeStamp = int(time.mktime(timeArray))
            origin = str1.split()[2]
            if 'item noimg' not in str(all[i]):  # 判断，若获取的cc值里面没有img标签，则结束本次循环
                # print(all[i])
                pic = all[i].find('img').get('src')
                title = all[i].find('div').find('a').text
                bean = NewsBean(url, title, content, timeStamp, origin, pic, time1)
                news_list.append(bean)
                continue
            pic = ""
            title = all[i].find('a').text
            bean = NewsBean(url, title, content, timeStamp, origin, pic, time1)
            news_list.append(bean)
        return news_list

    # 向外暴露的接口
    def go(self, type):
        htmls = self.__gethtml(type)
        return self.__analysis(htmls)
