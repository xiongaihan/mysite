from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Comment(models.Model):
	#获取外键的类型，是contentType，可以是任意的一个模型
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name='外键类型')
	#获取外键实例的id，例如博客对象的一个实际ID
	object_id = models.PositiveIntegerField(verbose_name='外联ID')
    #外联一个实际的对象，通过获取的模型类和实际的对象id
	content_object = GenericForeignKey('content_type', 'object_id')

	text=models.TextField(verbose_name='评论内容')
	comment_time=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
	# 需要设置related_name='root_comment'参数，user.comments可以获取当前user的所有相关的comment对象，如果不写，默认的是comment_set,如果有相同的外键，必须设置，否则将会报错。on_delete=models.CASCADE串联关系，当评论的用户被删除的时候，用户评论的内容也会被删除，可以保证数据的完整性
	user=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE,verbose_name='评论用户')

	#最顶级的评论，在最开始加载的时候，可以显示在最前面，通过反向关系获取，子集的评论对象
	root =models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
	#此评论的父级对象，可以是自己。
	parent=models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE)
	#此评论是回复那条评论的
	reply_to=models.ForeignKey(User,related_name='replies',null=True,on_delete=models.CASCADE)


	def get_user(self):
		return self.user


	def get_url(self):
		return self.content_object.get_url()

		
	class Meta(object):
		ordering=['comment_time']


	class Meta:
		#设置app的名称，会在显示的显示s复数
		verbose_name="评论"
		#复数的显示和单数一样
		verbose_name_plural=verbose_name
			
