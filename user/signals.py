from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from notifications.signals import notify


#注册接受器，注册通知
@receiver(post_save,sender=User)
def send_notifications(sender,instance,**kwargs):
	#判断只有注册的时候才会发送通知，其他例如修改密码，不通知
	if kwargs['created'] == True :
		verb='注册成功，更多精彩内容等你发现'

		url=reverse("user_info")
		#comment.user, 发送通知的用户，recipient=recipient,接受通知的用户，可以是多人，可以是列表类型 verb=verb,通知的信息action_object=comment触发通知的对象
		notify.send(instance, recipient=instance, verb=verb,action_object=instance,url=url)
		



 	
			

	