import os
from dotenv import load_dotenv as _load_dotenv

_load_dotenv()

N26_USERNAME = os.getenv('N26_USERNAME')
N26_PASSWORD = os.getenv('N26_PASSWORD')
N26_DEVICE_TOKEN = os.getenv('N26_DEVICE_TOKEN')
N26_LOGIN_DATA_STORE = os.getenv('N26_LOGIN_DATA_STORE', './.login_data')

FIREFLY_URL = os.getenv('FIREFLY_URL')
FIREFLY_TOKEN = os.getenv('FIREFLY_TOKEN')
FIREFLY_N26_ACCOUNT_ID = int(os.getenv('FIREFLY_N26_ACCOUNT_ID'))
FIREFLY_CASH_ACCOUNT_ID = int(os.getenv('FIREFLY_CASH_ACCOUNT_ID', -1))

LOOP_MINUTES = int(os.getenv('LOOP_MINUTES', 15))

COINTRACKING_COOKIE = os.getenv("COINTRACKING_COOKIE")
COINTRACKING_COOKIE2 = os.getenv("COINTRACKING_COOKIE2")
