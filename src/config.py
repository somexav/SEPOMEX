class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD ='12345'
    MYSQL_DB = 'sepomex_v1'

config = {
    'development': DevelopmentConfig
}