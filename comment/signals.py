import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
#将字符串总的html标签去掉
from django.utils.html import strip_tags
from django.conf import settings
# 将html模板转换为字符串
from django.template.loader import render_to_string
# 发送邮件的模块
from django.core.mail import send_mail
from notifications.signals import notify
from .models import Comment

@receiver(post_save,sender=Comment)
def send_notifications(sender,instance,**kwargs):

	#发送站内消息
		if instance.reply_to is None:
			#评论博客
			recipient=instance.content_object.get_user()
			if instance.content_type.model=='blog':
				blog=instance.content_object
				verb ='{0}评论了你的博客《{1}》'.format(instance.user.get_nickname_or_username(),blog.title)	
			else:
				raise Exception('unknown comment object type')
		else:
			#回复评论
			recipient=instance.reply_to
			verb='{0}回复了你的评论“{1}”'.format(instance.user.get_nickname_or_username(),strip_tags(instance.parent.text))

		#获取博客的链接
		url=instance.content_object.get_url()+"#comment_"+str(instance.pk)
		#comment.user, 发送通知的用户，recipient=recipient,接受通知的用户，可以是多人，可以是列表类型 verb=verb,通知的信息action_object=comment触发通知的对象
		notify.send(instance.user, recipient=recipient, verb=verb,action_object=instance,url=url)


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
		

@receiver(post_save,sender=Comment)
def send_email(sender,instance,**kwargs):

	# 发送邮件通知

	if instance.parent is None:
		# 评论我的博客
		subject='有人评论我的博客'
		# 获取邮箱
		email=instance.content_object.get_email()
	else:
		# 评论我的博客
		subject='有人回复你的评论'
		# 获取邮箱
		email=instance.reply_to.email
	if email !='':
		# 有二個參數reverse('blog_datail',kwargs={'blog_pk':comment.content_object.pk})反向解析當前的url，kwargs={'blog_pk':取決于url設置的關鍵字，不是隨便起的
		
		context={}
		context['text']=instance.text
		context['url']=instance.content_object.get_url()
		# 将模板页面的html转为字符串，将需要替换的数据传入，非常实用
		text=render_to_string('comment/send_mail.html',context)
		# 创建多线程的类
		send_email=SendEmail(subject,text,email)
		# 启动线程
		send_email.start()