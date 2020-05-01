from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'


    def ready(self):
    	super(UserConfig,self).ready()
    	from . import signals

    # 修改app的名称，还需在init。py文件中设置一下
    verbose_name = '个人简介'