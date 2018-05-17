# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('SCHOOL_SECRET', 'CyKSkRXhPawP_secret')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASKY_ADMIN = 'admin'
    REGISTERVERIFY = 'anaf'
    
    UPLOADED_PATH = 'data/uploads/'
    STUDENTS_IMG = 'data/students_img/'
    
    ALLOWED_EXTENSIONS_FILES = set(['png', 'jpg', 'jpeg', 'gif','xls','xlsx'])

    #测试号
    WECHAT_APPID = os.environ.get('SCHOOL_WECHAT_APPID') or 'wxb27de34ba5055b6b'
    WECHAT_SECRET = os.environ.get('SCHOOL_WECHAT_SECRET') or '1ea339c37b7e356ded9aea0da65d85'
    WECHAT_TOKEN = os.environ.get('SCHOOL_WECHAT_TOKEN') or 'wx_get_token_1234567890acb'
    # WECHAT_TOKEN = 'wx_get_token_1234567890acb'
    # WECHAT_SECRET = '1ea339c37b7e356def3d9aea0da65d85'
    # WECHAT_APPID = 'wxb27de34ba5055b6b'
    

    AIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '000'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '000'
    MAIL_DEBUG = False


    


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('prod_school_database_url') or \
        'mysql://root:@127.0.0.1:3306/school'
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    # DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = os.environ.get('prod_school_database_url') or \
        'mysql://root:@127.0.0.1:3306/school'
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
