# 服务器配置文件
# 服务器配置
DEBUG = True
PORT = 9082
IP = '127.0.0.1'

# 数据库配置
DB_USERNAME = 'root'
DB_PASS = '123456'
DB_PORT = '3306'
DB_IP = "127.0.0.1"
DB_NAME = 'news'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(
    username=DB_USERNAME,
    password=DB_PASS,
    host=DB_IP, port=DB_PORT,
    db=DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
