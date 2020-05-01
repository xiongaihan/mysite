from django.apps import AppConfig


class LikesConfig(AppConfig):
    name = 'likes'


    def ready(self):
    	super(LikesConfig,self).ready()
    	from . import signals

    # 修改app的名称，还需在init。py文件中设置一下
    verbose_name = '点赞'