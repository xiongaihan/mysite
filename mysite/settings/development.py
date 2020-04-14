"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
# 引入公共的部分
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#原来的方法如下
#SECRET_KEY = '0$nageb841@fk=w2!$y!(5abun9^wg)eh26irai1lt$5456!-&'
#新的安全方法
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

'''
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']

#'PASSWORD': 'xx5201314',
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql_db',
        'USER': 'xiongxing',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


#EMAIL_HOST_PASSWORD = 'ycuwbgzbovmobbcc'    #授权码
EMAIL_HOST_PASSWORD=os.environ['EMAIL_HOST_PASSWORD']
# 发送邮件的设置
# 文档链接https://docs.djangoproject.com/en/2.0/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True  #与smtp服务器通信时，是否启动TLS链接（安全链接）
EMAIL_HOST = 'smtp.qq.com' #发送邮件的服务器的地址
EMAIL_PORT = 25                    #服务的端口号
EMAIL_HOST_USER = '948709909@qq.com' #发送地址
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD    #授权码
DEFAULT_FROM_EMAIL = '熊星<948709909@qq.com>'