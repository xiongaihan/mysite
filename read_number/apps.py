from django.apps import AppConfig


class ReadNumberConfig(AppConfig):
    name = 'read_number'
    # 修改app的名称，还需在init。py文件中设置一下
    verbose_name = '阅读'
