SECRET_KEY = 'aeivnew,;r'

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_demo'
USERNAME = 'root'
PASSWORD = '1234'
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = "smtp.163.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "arulhz@163.com"
MAIL_PASSWORD = "CKIVSOZHAWQWIUBW"
MAIL_DEFAULT_SENDER = "arulhz@163.com"
