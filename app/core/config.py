import os

# ================ Project ================
PROJECT_NAME = str(os.environ.get('PROJECT_NAME'))

# ================ Mysql ================
DB_TYPE = str(os.environ.get('DB_TYPE'))
USERNAME = str(os.environ.get('USERNAME'))
PASSWORD = str(os.environ.get('PASSWORD'))
HOST = str(os.environ.get('HOST'))
PORT = int(os.environ.get('PORT'))
DATABASE = str(os.environ.get('DATABASE'))
