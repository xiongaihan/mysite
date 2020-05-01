from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
#导入错误模块
from django.db.models.fields import exceptions
#引入django的工具集
from django.utils import timezone

class ReadNum(models.Model):
	#此属性是自己随便定义的
	read_num=models.IntegerField(default=0)

	#获取外键的类型，是contentType，可以是任意的一个模型
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	#获取外键实例的id，例如博客对象的一个实际ID
	object_id = models.PositiveIntegerField()
    #外联一个实际的对象，通过获取的模型类和实际的对象id
	content_object = GenericForeignKey('content_type', 'object_id')


	class Meta:
		#设置app的名称，会在显示的显示s复数
		verbose_name="阅读数量"
		#复数的显示和单数一样
		verbose_name_plural=verbose_name

#将计数的内容放在一起，此方法为计数拓展的方法
class ReadNumExpandMethod(object):

	def get_read_num(self):
		try:
			#注意model的后面不要加s，否则会报错！
			ct=ContentType.objects.get_for_model(self)
			readnum=ReadNum.objects.get(content_type=ct,object_id=self.pk)
			return readnum.read_num
		except exceptions.ObjectDoesNotExist as e:
			return 0


#创建阅读量当日的详情
class ReadDetail(models.Model):
	#此属性是自己随便定义的
	read_num=models.IntegerField(default=0)
	#引入时间字段，默认是当前服务器的时间，只是日期，不带时间
	date=models.DateField(default=timezone.now)

	#获取外键的类型，是contentType，可以是任意的一个模型
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	#获取外键实例的id，例如博客对象的一个实际ID
	object_id = models.PositiveIntegerField()
    #外联一个实际的对象，通过获取的模型类和实际的对象id
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		#设置app的名称，会在显示的显示s复数
		verbose_name="阅读详情"
		#复数的显示和单数一样
		verbose_name_plural=verbose_name


		
		
		
