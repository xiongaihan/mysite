from django.db.models.signals import post_save
from django.dispatch import receiver
#将字符串总的html标签去掉
from django.utils.html import strip_tags
from notifications.signals import notify
from .models import LikeRecord


#注册接受器，点赞通知
@receiver(post_save,sender=LikeRecord)
def send_notifications(sender,instance,**kwargs):
	if instance.content_type.model == 'blog':
		blog=instance.content_object
		verb ='{0}点赞了你的博客《{1}》'.format(instance.user.get_nickname_or_username(),blog.title)
	elif instance.content_type.model =='comment':
		comment=instance.content_object
		verb='{0}点赞了你的评论“{1}”'.format(instance.user.get_nickname_or_username(),strip_tags(comment.text))
	

	recipient=instance.content_object.get_user()

	url=instance.content_object.get_url()
	#comment.user, 发送通知的用户，recipient=recipient,接受通知的用户，可以是多人，可以是列表类型 verb=verb,通知的信息action_object=comment触发通知的对象
	notify.send(instance.user, recipient=recipient, verb=verb,action_object=instance,url=url)



 	
			

	