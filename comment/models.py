import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
# 发送邮件的模块
from django.core.mail import send_mail
# 将html模板转换为字符串
from django.template.loader import render_to_string



# 继承线程的类
class SendEmail(threading.Thread):

	# 初始化方法
	def __init__(self,subject,text,email,fail_silently=False):
		self.subject=subject
		self.text=text
		self.email=email
		self.fail_silently=fail_silently
		# 继承的父类必写
		threading.Thread.__init__(self)


	# 重写run方法，将耗时的操作放在这里
	def run(self):
		send_mail(
			self.subject,
			'',
			settings.
			DEFAULT_FROM_EMAIL,
			[self.email],
			fail_silently=self.fail_silently,
			html_message=self.text
		)
	# 返回的是html内容
		

class Comment(models.Model):
	#获取外键的类型，是contentType，可以是任意的一个模型
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name='外键类型')
	#获取外键实例的id，例如博客对象的一个实际ID
	object_id = models.PositiveIntegerField(verbose_name='外联ID')
    #外联一个实际的对象，通过获取的模型类和实际的对象id
	content_object = GenericForeignKey('content_type', 'object_id')

	text=models.TextField(verbose_name='评论内容')
	comment_time=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
	# 需要设置related_name='root_comment'参数，如果有相同的外键，必须设置，否则将会报错。on_delete=models.CASCADE串联关系，当评论的用户被删除的时候，用户评论的内容也会被删除，可以保证数据的完整性
	user=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE,verbose_name='评论用户')

	#最顶级的评论，在最开始加载的时候，可以显示在最前面，通过反向关系获取，子集的评论对象
	root =models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
	#此评论的父级对象，可以是自己。
	parent=models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE)
	#此评论是回复那条评论的
	reply_to=models.ForeignKey(User,related_name='replies',null=True,on_delete=models.CASCADE)


	# 发送邮件的方法
	def send_mail(self):
		# 发送邮件通知

		if self.parent is None:
			# 评论我的博客
			subject='有人评论我的博客'
			# 获取邮箱
			email=self.content_object.get_email()
		else:
			# 评论我的博客
			subject='有人回复你的评论'
			# 获取邮箱
			email=self.reply_to.email
		if email !='':
			# 有二個參數reverse('blog_datail',kwargs={'blog_pk':comment.content_object.pk})反向解析當前的url，kwargs={'blog_pk':取決于url設置的關鍵字，不是隨便起的
			
			context={}
			context['text']=self.text
			context['url']=self.content_object.get_url()
			# 将模板页面的html转为字符串，将需要替换的数据传入，非常实用
			text=render_to_string('comment/send_mail.html',context)
			# 创建多线程的类
			send_email=SendEmail(subject,text,email)
			# 启动线程
			send_email.start()

		
	class Meta(object):
		ordering=['comment_time']
			
