from flask import Flask, request
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from spider import Spider

# 初始化Flask对象
app = Flask(__name__)
# 读取配置文件
app.config.from_object('config')
# 初始化数据库
engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'], max_overflow=5)
conn = engine.connect()
Base = declarative_base()
db = SQLAlchemy(app)


# 创建头条新闻表
class NewsTop(Base):
    __tablename__ = "top"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100), nullable=False)  # 文章详细内容链接
    title = db.Column(db.String(100), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # 内容
    time = db.Column(db.Text, nullable=False)  # 时间,用于进行比较的
    formattime = db.Column(db.Text, nullable=False)  # 格式化的时间
    origin = db.Column(db.Text, nullable=False)  # 来源
    pic = db.Column(db.Text, nullable=False)  # 图片地址


# 创建国际新闻表
class NewsWorld(Base):
    __tablename__ = "world"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100), nullable=False)  # 文章详细内容链接
    title = db.Column(db.String(100), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # 内容
    time = db.Column(db.Text, nullable=False)  # 时间,用于进行比较的
    formattime = db.Column(db.Text, nullable=False)  # 格式化的时间
    origin = db.Column(db.Text, nullable=False)  # 来源
    pic = db.Column(db.Text, nullable=False)  # 图片地址


# 创建用户表
class User(Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)  # 用户名
    password = db.Column(db.String(100), nullable=False)  # 密码


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# 向数据库添加国际新闻数据
def add_world_data():
    splder = Spider()
    new_list = splder.go('world')
    ret = session.query(NewsWorld).order_by(NewsWorld.id.desc()).first()  # 查询时间最大的那条数据
    for new in new_list:
        if ret is not None and int(ret.time) >= new.time:
            continue
        else:
            article = NewsWorld(url=new.url, title=new.title, content=new.content, time=new.time,
                                origin=new.origin, pic=new.pic, formattime=new.formattime)
            session.add(article)
            session.commit()


# 向数据库添加头条新闻数据
def add_top_data():
    splder = Spider()
    new_list = splder.go('top')
    ret = session.query(NewsTop).order_by(NewsTop.id.desc()).first()  # 查询时间最大的那条数据
    for new in new_list:
        if ret is not None and int(ret.time) >= new.time:
            continue
        else:
            article = NewsTop(url=new.url, title=new.title, content=new.content, time=new.time,
                              origin=new.origin, pic=new.pic, formattime=new.formattime)
            session.add(article)
            session.commit()


# 需要执行的循环任务
def add_data():
    add_top_data()
    add_world_data()


@app.route('/query/<string:type>', methods=['GET', 'POST'])
def query(type):
    if type == 'top':
        lasttime = 0 if request.args.get('lasttime') is None else request.args.get('lasttime')
        retmax = session.query(NewsTop).order_by(NewsTop.id.desc()).first()  # 查询时间最大的那条数据
        ret = session.query(NewsTop).order_by(NewsTop.id.desc()).limit(10)
    else:
        if type == 'world':
            lasttime = 0 if request.args.get('lasttime') is None else request.args.get('lasttime')
            retmax = session.query(NewsWorld).order_by(NewsWorld.id.desc()).first()  # 查询时间最大的那条数据
            ret = session.query(NewsWorld).order_by(NewsWorld.id.desc()).limit(10)
        else:
            return "访问路径错误"

    list = []
    jsonreturn = {}
    if retmax is None:
        return jsonreturn
    jsonreturn["lasttime"] = retmax.time
    for i in range(10):
        json = {}
        if int(lasttime) > int(ret[i + 1].time):
            continue
        json["time"] = ret[i + 1].time
        json["url"] = ret[i + 1].url
        json["title"] = ret[i + 1].title
        json["content"] = ret[i + 1].content
        json["time"] = ret[i + 1].time
        json["formattime"] = ret[i + 1].formattime
        json["origin"] = ret[i + 1].origin
        json["pic"] = ret[i + 1].pic
        list.append(json)

    jsonreturn["data"] = list

    # if lasttime == 0:
    #
    # else:
    #     ret = session.query(NewsContent).order_by(NewsContent.id.desc()).limit(10)
    return jsonreturn


# 登录
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        username = request.args.get('username')
    else:
        username = request.json['username']
    print(request.json)
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        return "用户名不存在,请注册"
    else:
        password = request.args.get('password')
        if password == user.password:
            return "登录成功"
        else:
            return "密码错误"


# 注册
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        username = request.args.get('username')
    else:
        username = request.json['username']
    user = session.query(User).filter_by(username=username).first()
    if user is not None:
        return "用户名存在,请登录"
    else:
        password = request.args.get('password')
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        return "注册成功"


if __name__ == '__main__':
    # 创建任务循环,每一个小时去爬取
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.add_job(func=add_data, id='1', args=(), trigger='interval', seconds=1 * 60 * 60, replace_existing=True)
    scheduler.start()
    # 运行
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['IP'])
