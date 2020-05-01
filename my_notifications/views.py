from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from notifications.models import Notification


# 消息中心的方法
def my_notifications(request):
	context={}
	return render(request,'my_notifications/my_notifications.html',context)

# 全部消息标记为已读的方法
def my_notification(request,my_notification_pk):
	my_notification=get_object_or_404(Notification,pk=my_notification_pk)
	my_notification.unread=False
	my_notification.save()
	if not my_notification.data == None:
		return redirect(my_notification.data['url'])
	return redirect(reverse('home'))


#将已读的信息全部删除
def delete_my_read_notifications(request):
	# 获取所有的已读消息集合
	notifications=request.user.notifications.read()
	#将已读消息集合删除
	notifications.delete()
	#重定向到消息中心
	return redirect(reverse('my_notifications'))