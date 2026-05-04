class Config:
    SECRET_KEY = 'test'

    # Настройки MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@localhost/metod'
    SQLALCHEMY_TRACK_MODIFICATIONS = False