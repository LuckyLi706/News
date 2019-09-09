import json
from flask_apscheduler import APScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from spider import Spider

# 初始化Flask对象
app = Flask(__name__)
# 读取配置文件
app.config.from_object('config')
print(type(app.config['DB_PORT']))
# 初始化数据库
engine = create_engine(
    "mysql+pymysql://" + app.config['DB_USERNAME'] + ":" + app.config['DB_PASS'] + "@" + app.config['DB_IP'] + ":" +
    app.config['DB_PORT'] + "/news", max_overflow=5)
Base = declarative_base()
db = SQLAlchemy(app)


# 创建表
class Article(Base):
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100), nullable=False)  # 文章详细内容链接
    title = db.Column(db.String(100), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # 内容
    time = db.Column(db.Text, nullable=False)  # 时间,用于进行比较的
    formattime = db.Column(db.Text, nullable=False)  # 格式化的时间
    origin = db.Column(db.Text, nullable=False)  # 来源
    pic = db.Column(db.Text, nullable=False)  # 图片地址


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# 需要执行的循环任务
def add_data():
    splder = Spider()
    new_list = splder.go()
    ret = session.query(Article).order_by(Article.id.desc()).first()  # 查询时间最大的那条数据
    for new in new_list:
        if ret is not None and int(ret.time) >= new.time:
            continue
        else:
            article = Article(url=new.url, title=new.title, content=new.content, time=new.time,
                              origin=new.origin, pic=new.pic, formattime=new.formattime)
            session.add(article)
            session.commit()


@app.route('/')
def query():
    ret = session.query(Article).order_by(Article.id.desc()).first()
    return str(ret.time)


if __name__ == '__main__':
    # 创建任务循环,每一个小时去爬取
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.add_job(func=add_data, id='1', args=(), trigger='interval', seconds=1 * 60 * 60, replace_existing=True)
    scheduler.start()

    # 运行
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['IP'])
