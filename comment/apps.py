from django.apps import AppConfig


class CommentConfig(AppConfig):
    name = 'comment'

    def ready(self):
    	super(CommentConfig,self).ready()
    	from . import signals

    # 修改app的名称，还需在init。py文件中设置一下
    verbose_name = '评论'