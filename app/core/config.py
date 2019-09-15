import os

from dotenv import load_dotenv

load_dotenv()

# ================ Project ================
PROJECT_NAME = str(os.environ.get('PROJECT_NAME'))

# ================ Mysql ================
DB_TYPE = str(os.environ.get('DB_TYPE'))
DB_USER = str(os.environ.get('DB_USERNAME'))
DB_PASSWORD = str(os.environ.get('DB_PASSWORD'))
DB_HOST = str(os.environ.get('DB_HOST'))
DB_PORT = int(os.environ.get('DB_PORT'))
DATABASE = str(os.environ.get('DB_DATABASE'))
