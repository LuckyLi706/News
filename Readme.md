# 使用Flask+MySQL写定时任务的爬虫
每隔1小时去爬取网站的新闻信息,并将其保存到MySQL数据库中
## 需要的包
+ Flask
+ SQLAlchemy
+ Flask_APScheduler
+ Flask_SQLAlchemy
+ bs4
+ Flask_pymysql
## 运行
1. 创建数据库news
2. python app.py