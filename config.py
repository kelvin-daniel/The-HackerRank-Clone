class Config():
    '''
    General app configuration 
    '''

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@localhost/hackerrank'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


config_options = {
    'development' : DevConfig,
    'production' : ProdConfig
}