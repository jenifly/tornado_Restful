import os

# Application
settings = dict(
    cookie_secret = 'ko09mvDRTFWkcHWt3wHi+sww0r6vsE5mm/1wnFfGGVA=',
    compiled_template_cache = False,
    xsrf_cookies = True,
    debug = True
)

# mysql
mysql_options = dict(
    host='jenifly.xyz',
    db='blog',
    user='jenifly',
    password='0926.',
    charset="utf8"
)

# redis
redis_options = dict(
    address=('jenifly.xyz', 6379)
)

# path
path = os.path.dirname(__file__)
ufiles_path = os.path.join(path, 'ufiles')
res_path = os.path.join(path, 'res')

# log
log_path = os.path.join(path, 'logs/log')
log_level = 'error'

# Cryptographic key
PASSWD_HASH_KEY = 'JfLpppukEemTdeDVXmfHzyXy6aebpBHphHfg1V5nx88='
# base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

# IMG_CODE
IMG_CODE_EXPIRES_SECONDS = 90
IMG_CODE_WIDTH = 200
IMG_CODE_HEIGHT = 75

# session
SESSION_PREFIX = 'zj_s_'
SESSION_EXPIRES_SECONDS = 2592000
SEESION_HASH_KEY = 'UrDFVYV2TA6tZaYuIlIh4COPawd9N0Q3gya7V48AcBM='
