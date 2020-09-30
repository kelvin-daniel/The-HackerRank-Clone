class Config():
    '''
    General app configuration 
    '''

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://timothy:index506119056@localhost/hackerrank'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


config_options = {
    'development' : DevConfig,
    'production' : ProdConfig
}