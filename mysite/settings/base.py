"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))





# Application definition
#可以注册第三方的模型‘ckeditor’
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'blog',
    'read_number',
    'comment',
    'likes',
    'user',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'
#设置模板信息
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.login_modal_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
#设置简体中文显示
LANGUAGE_CODE = 'zh-hans'

#美国时间
#TIME_ZONE = 'UTC'

#中国时间
TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#创建静态文件的地址，否则无法访问静态文件
STATIC_URL = '/static/'
#收集静态文件，主要用于服务器的
STATIC_ROOT=os.path.join(BASE_DIR,'static_collected')

#git测试


STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static'),

]

#配置media的ULR，网页显示的地址，专门储存上传的文件
MEDIA_URL='/media/'
#配置media在服务器的位置类型静态文件
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

#配置ckeditor的上传文件,会在media文件夹下再创建一个文件夹
CKEDITOR_UPLOAD_PATH='upload/'

#配置ckeditor,'removePlugins':'elementspath',去掉下框，'resize_enabled':False,尺寸不可改变,需要设置default，否则未命名的编辑框会报错
CKEDITOR_CONFIGS = {
    'default':{},
    'comment_ckeditor': {
        'toolbar': 'custom',
        'toolbar_custom':[
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['TextColor', 'BGColor','RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Smiley', 'SpecialChar','Blockquote']

        ],
        'height': 180,
        'width': 'auto',
        'tabSpaces':4,
        'removePlugins':'elementspath',
        'resize_enabled':False,
    },
}

#自定义参数,设置每页的博客数量
EACH_PAGE_BLOGS_NUMBER=10

#设置缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}


