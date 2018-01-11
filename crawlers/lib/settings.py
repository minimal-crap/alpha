# mysql database params
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Alpha123#'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'crawler_db'
MYSQL_CHARSET = 'utf8mb4'

MYSQL_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
    MYSQL_USER, MYSQL_PASSWORD,
    MYSQL_HOST, MYSQL_PORT,
    MYSQL_DB, MYSQL_CHARSET
)

# user agent list to randomly choose from while crawling
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",  # noqa
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",  # noqa
    "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
    "Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0", ]
# proxies can be set here as an extra precaution while crawling
# for example:
# PROXIES = {
#    'http': 'http://127.0.0.1:8123'
#}

PROXIES = None
