from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class LikeCount(models.Model):
	#获取外键的类型，是contentType，可以是任意的一个模型
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name='外键类型')
	#获取外键实例的id，例如博客对象的一个实际ID
	object_id = models.PositiveIntegerField(verbose_name='外联ID')
    #外联一个实际的对象，通过获取的模型类和实际的对象id
	content_object = GenericForeignKey('content_type', 'object_id')

	liked_num=models.IntegerField(default=0)

	class Meta:
		#设置app的名称，会在显示的显示s复数
		verbose_name="点赞数量"
		#复数的显示和单数一样
		verbose_name_plural=verbose_name




class LikeRecord(models.Model):
	
	#获取外键的类型，是contentType，可以是任意的一个模型
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name='外键类型')
	#获取外键实例的id，例如博客对象的一个实际ID
	object_id = models.PositiveIntegerField(verbose_name='外联ID')
    #外联一个实际的对象，通过获取的模型类和实际的对象id
	content_object = GenericForeignKey('content_type', 'object_id')

	# 需要设置related_name='root_comment'参数，如果有相同的外键，必须设置，否则将会报错。on_delete=models.CASCADE串联关系，当评论的用户被删除的时候，用户评论的内容也会被删除，可以保证数据的完整性
	user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='点赞用户')
	liked_time=models.DateTimeField(auto_now_add=True)


	class Meta:
		#设置app的名称，会在显示的显示s复数
		verbose_name="点赞记录"
		#复数的显示和单数一样
		verbose_name_plural=verbose_name
