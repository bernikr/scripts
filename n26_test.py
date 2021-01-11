from n26.api import Api
from n26.config import Config
from settings import *

conf = Config(validate=False)
conf.USERNAME.value = N26_USERNAME
conf.PASSWORD.value = N26_PASSWORD
conf.LOGIN_DATA_STORE_PATH.value = N26_LOGIN_DATA_STORE
conf.MFA_TYPE.value = "app"
conf.DEVICE_TOKEN.value = N26_DEVICE_TOKEN
conf.validate()

if __name__ == '__main__':
    api_client = Api(conf)
    print(api_client.get_transactions())
