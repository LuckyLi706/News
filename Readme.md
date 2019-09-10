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
## 主要接口
### 查询数据接口
http://127.0.0.1:9080/query?lasttime=1568085420
+ lasttime参数非必须参数,不带会返回最新的10条数据
+ lasttime携带表示返回这个时间点之后的数据,用于做数据更新,每次请求都会返回一个lasttime,
每次请求最多返回10条数据。
+ 返回数据内容
````
{
    "data": [
        {
            "content": "  \n                  阿富汗塔利班组织8日说，美国总统唐纳德·特朗普取消与塔利班代表对话的决定“只会让美方承受更多损失”。\n塔利班发言人扎比乌拉·穆...                                 ",
            "formattime": "2019-09-10 10:46",
            "origin": "来源:新华网",
            "pic": "",
            "time": "1568083560",
            "title": "塔利班回应特朗普取消会面：美方承受更多损失",
            "url": "http://www.mnw.cn/news/world/2198066.html"
        },
        {
            "content": "  \n                  新华社华盛顿9月9日电（记者高攀 熊茂伶）国际货币基金组织（IMF）执行董事会9日宣布世界银行首席执行官克里斯塔利娜·格奥尔基耶娃为下任IMF总裁的唯一提...                                 ",
            "formattime": "2019-09-10 10:46",
            "origin": "来源:新华网",
            "pic": "",
            "time": "1568083560",
            "title": "格奥尔基耶娃成为IMF下任总裁唯一提名人选",
            "url": "http://www.mnw.cn/news/world/2198065.html"
        },
        {
            "content": "  \n                  土耳其国防部8日证实，土耳其军队当天出动装甲车，从东南部边境进入叙利亚北部，与驻扎在那里的美国军队一同执行地面巡逻。按照土美两国媒体的说法，这是双方地面...                                 ",
            "formattime": "2019-09-10 10:45",
            "origin": "来源:新华网",
            "pic": "",
            "time": "1568083500",
            "title": "土美地面部队首次在叙利亚“安全区”联合巡逻",
            "url": "http://www.mnw.cn/news/world/2198064.html"
        },
        {
            "content": "  \n                  伊朗外交部一名发言人8日说，伊方可能“很快”释放一艘英国油轮。\n这名发言人同时披露，一艘先前遭英方扣押的伊朗油轮已经停靠在地中海地区并开始&...                                 ",
            "formattime": "2019-09-10 10:45",
            "origin": "来源:新华网",
            "pic": "",
            "time": "1568083500",
            "title": "伊朗可能“很快”释放英国油轮 已进入“最终阶段”",
            "url": "http://www.mnw.cn/news/world/2198062.html"
        },
        {
            "content": "  \n                  【人类首次感染艾滋病毒时间或被提前】美国亚利桑那大学的演化生物学家们在一份1966年淋巴结样本中，提取出了HIV-1型病毒近乎完整的的基因组，这是目前发现时间最...                                 ",
            "formattime": "2019-09-10 10:32",
            "origin": "来源:Vista看天下",
            "pic": "http://upload.mnw.cn/2019/0910/thumb_120_80_1568082726315.jpg",
            "time": "1568082720",
            "title": "人类首次感染艾滋病毒时间或被提前至1896-1905年间",
            "url": "http://www.mnw.cn/news/world/2198049.html"
        },
        {
            "content": "  \n                  中国日报网9月10日电（严玉洁）8月末，英国首相鲍里斯·约翰逊提出议会休会请求，并得到女王伊丽莎白二世批准。根据该请求，议会在9月9日至12日期间择日开...                                 ",
            "formattime": "2019-09-10 11:43",
            "origin": "来源:中国日报网",
            "pic": "",
            "time": "1568086980",
            "title": "英国政府70多年来首次叫停议会 休会至10月14日",
            "url": "http://www.mnw.cn/news/world/2198146.html"
        },  
    ],
    "lasttime": "1568086980"
}
````
## 其他接口
### 注册接口(支持get和post请求)
http://127.0.0.1:9080/register?username=lijie&password=1234
### 登录接口(支持get和post接口)
http://127.0.0.1:9080/login?username=lijie&password=1234