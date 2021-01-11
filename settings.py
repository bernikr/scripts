import os
from dotenv import load_dotenv

load_dotenv()

N26_USERNAME = os.getenv('N26_USERNAME')
N26_PASSWORD = os.getenv('N26_PASSWORD')
N26_DEVICE_TOKEN = os.getenv('N26_DEVICE_TOKEN')
N26_LOGIN_DATA_STORE = os.getenv('N26_LOGIN_DATA_STORE', './.login_data')
