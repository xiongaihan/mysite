from django.shortcuts import render,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
#导入json对象
from django.http import JsonResponse
#发送信息模块
from notifications.signals import notify
from .forms import CommentForm
import datetime


def update_comment(request):

	'''#得到请求的地址，如果没有的话，返回首页
	referer=request.META.get('HTTP_REFERER',reverse('home'))
	user=request.user
	#数据检查
	# 判断用户是否登录
	if not request.user.is_authenticated:
		return render(request,'error.html',{'message':"用户未登录",'redirect_to':referer})
	text=request.POST.get('text','')
	# 如果评论的内容为空，返回一个错误的页面
	if text=='':
		return render(request,'error.html',{'message':"评论内容不能为空",'redirect_to':referer})

	try:
		content_type=request.POST.get('content_type','')
		#将字符串转换为数字
		object_id=int(request.POST.get('object_id',''))
		# ContentType.objects.get(model=content_type)获取model为blog的ContentType对象，model_class=ContentType.objects.get(model=content_type).model_class()获取blog的全部对象
		model_class=ContentType.objects.get(model=content_type).model_class()
		# 获取主键为object——id的blog对象
		model_obj=model_class.objects.get(pk=object_id)
	except Exception as e:
		return render(request,'error.html',{'message':"评论对象不存在",'redirect_to':referer})
	
	#检查通过，保存数据
	comment=Comment()
	comment.user=user
	comment.text=text
	comment.content_object=model_obj
	comment.save()

	
	return redirect(referer)'''

	#得到请求的地址，如果没有的话，返回首页
	referer=request.META.get('HTTP_REFERER',reverse('home'))
	# 根据提交的内容，实例化一个对象
	comment_form=CommentForm(request.POST,user=request.user)
	# 返回数据
	data={}
	if comment_form.is_valid():
		#检查通过，保存数据
		comment=Comment()
		comment.user=comment_form.cleaned_data['user']
		comment.text=comment_form.cleaned_data['text']
		comment.content_object=comment_form.cleaned_data['content_object']

		# 验证以后取出parent对象
		parent=comment_form.cleaned_data['parent']

		#如果父类不为空
		if not parent is None:
			#添加顶级评论，如果parent没有顶级评论，则将父类赋给顶级评论，例如直接回复顶级评论的评论，父类就是顶级评论
			comment.root=parent.root if not parent.root is None else parent
			comment.parent=parent
			#回复就是父类用户
			comment.reply_to=parent.user
		#保存数据到数据库
		comment.save()


		
		

		# 返回数据
		data['status']='SUCCESS'
		# 动态属性是一个方法，在前端模板页面可以不加（）号
		data['username']=comment.user.get_nickname_or_username()
		#将当前的时间传入，否则将会显示UTC的时间，系统默认的写入时间是UTC的时间
		now = datetime.datetime.now()
		#需要将时间转为字符
		data['comment_time']=now.strftime('%Y-%m-%d %H:%M:%S')
		data['text']=comment.text
		# 返回一个字符对象
		data['content_type']=ContentType.objects.get_for_model(comment).model

		if not parent is None:
			data['reply_to']=comment.reply_to.get_nickname_or_username()
		else:
			data['reply_to']=''
		data['pk']=comment.pk
		data['root_pk']=comment.root.pk if not comment.root is None else ''


		# return redirect(referer)

	else:
		# return render(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})
		data['status']='ERROR'
		data['message']=list(comment_form.errors.values())[0]


	return JsonResponse(data)
