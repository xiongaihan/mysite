from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    # 修改app的名称，还需在init。py文件中设置一下
    verbose_name = '博客'
