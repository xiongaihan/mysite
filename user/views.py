import string
import random
import time

# 带HTML格式和附件的邮件发送
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render,get_object_or_404,redirect
#引入验证和登录的方法
from django.contrib import auth
from django.http import JsonResponse
from django.urls import reverse
# 发送邮件的模块
from django.core.mail import send_mail
from .forms import LoginForm,RegForm,ChangeNicknameForm,BindEmailForm,ChangePasswordForm,ForgotPasswordForm
#导入用户对象
from django.contrib.auth.models import User
from .models import Profile




def login(request):
	'''username=request.POST.get('username','')
	password=request.POST.get('password','')
	#验证用户是否存在
	user = auth.authenticate(request, username=username, password=password)
	#得到请求的地址，如果没有的话，返回首页
	referer=request.META.get('HTTP_REFERER',reverse('home'))
	#如果用户存在，返回对象
	if user is not None:
		#登录
	    auth.login(request, user)
	    #重定向到请求的网址，否则返回首页。
	    return redirect(referer)
	else:
		#返回到一个错误的页面
	    return render(request,'error.html',{'message':"用户名或者密码不正确"})'''
	   # 判断请求的类型为post的时候
	if request.method=='POST':
		#通过前端提交的信息，实例化一个form对象，前端信息返回
		login_form=LoginForm(request.POST)
		#如果前端输入的信息都是有效的，符合字段规范，执行类中的clean验证方法
		if login_form.is_valid():
			user=login_form.cleaned_data['user']
			auth.login(request,user)
			return redirect(request.GET.get('from',reverse('home')))
		
			#添加一个错误的提示信息
			#login_form.add_error(None,'用户名或者密码不正确')


	# 为get请求的时候，直接加载界面
	else:
		login_form=LoginForm()
	context={}
	context['login_form']=login_form
	return render(request,'user/login.html',context)

def login_for_modal(request):

	#通过前端提交的信息，实例化一个form对象，前端信息返回
	login_form=LoginForm(request.POST)
	data={}
	#如果前端输入的信息都是有效的，符合字段规范，执行类中的clean验证方法
	if login_form.is_valid():
		user=login_form.cleaned_data['user']
		auth.login(request,user)
		data['status']='SUCCESS'
	else:
		data['status']='ERROR'

	return JsonResponse(data)


def register(request):
	if request.method=='POST':
		#通过前端提交的信息，实例化一个form对象，前端信息返回
		reg_form=RegForm(request.POST,request=request)
		#如果前端输入的信息都是有效的，符合字段规范，执行类中的clean验证方法
		if reg_form.is_valid():
			username=reg_form.cleaned_data['username']
			email=reg_form.cleaned_data['email']
			password=reg_form.cleaned_data['password']
			#创建用户
			user=User.objects.create_user(username,email,password)
			#将用户保存到数据库
			user.save()
			# 清除session,否则一直可以可以使用！是个bug
			del request.session[email]
			#登录用户
			auth.login(request,user)
			return redirect(request.GET.get('from',reverse('home')))
		
			#添加一个错误的提示信息
			#login_form.add_error(None,'用户名或者密码不正确')


	# 为get请求的时候，直接加载界面
	else:
		reg_form=RegForm()
	context={}
	context['reg_form']=reg_form
	return render(request,'user/register.html',context)
	


def logout(request):
	auth.logout(request)
	return redirect(request.GET.get('from',reverse('home')))



def user_info(request):
	context={}
	context['from']=request.GET.get('from')
	return render(request,'user/user_info.html',context)


def user_back(request):
	print("开始")
	print(request.GET.get('from',reverse('home')))
	return redirect(request.GET.get('from',reverse('home')))


def change_nickname(request):
	# 返回链接
	redirect_to=redirect(request.GET.get('from',reverse('home')))
	if request.method =='POST':
		form=ChangeNicknameForm(request.POST,user=request.user)
		if form.is_valid():
			nickname_new=form.cleaned_data['nickname_new']
			# 获取对象或者创建新的对象
			profile,created=Profile.objects.get_or_create(user=request.user)
			profile.nickname=nickname_new
			profile.save()
			return redirect_to
	else:
		form=ChangeNicknameForm()

	context={}
	context['form']=form
	context['page_title']='修改昵称'
	context['form_title']='修改昵称'
	context['submit_text']='修改'
	context['retrun_back']=redirect_to

	return render(request,'form.html',context)


def bind_email(request):
	# 返回链接
	redirect_to=redirect(request.GET.get('from',reverse('home')))
	if request.method =='POST':
		form=BindEmailForm(request.POST,request=request)
		if form.is_valid():
			email_new=form.cleaned_data['email']
			request.user.email=email_new
			request.user.save()
			# 清除session
			del request.session[email_new]
			return redirect_to
	else:
		form=BindEmailForm()

	context={}
	context['form']=form
	context['page_title']='绑定邮箱'
	context['form_title']='绑定邮箱'
	context['submit_text']='绑定'
	context['retrun_back']=redirect_to

	return render(request,'user/bind_email.html',context)

# https://docs.djangoproject.com/en/2.0/topics/email/邮件发送文档
def send_verification_code(request):
	email=request.GET.get('email','')
	data={}
	print('发送验证码的邮箱：'+email)
	if email!='':
		# 生成验证码,random.sample(string.ascii_letters+string.digits,4)随机生成0-9和a-z的4个元素的列表
		code =''.join(random.sample(string.ascii_letters+string.digits,4))

		now=int(time.time())
		send_code_time=request.session.get('send_code_time',0)
		print('生成的随机验证码：'+code)
		if now - send_code_time <30 :
			data['status']='ERROR'

		else:
			# 设置访问用户的session，将email设置为key
			request.session[email]=code
			request.session['send_code_time']=now
			send_mail(
			    '绑定邮箱',
			 	'<p>这是一封<strong>重要的</strong>邮件.</p>验证码：%s'%code,
				'熊星<948709909@qq.com>',
				[email],
				fail_silently=False,
			)
			data['status']='SUCCESS'
	else:
		data['status']='EEROR'

	# msg = EmailMultiAlternatives('带HTML的邮件', '<p>这是一封<strong>重要的</strong>邮件.</p>', '熊星<948709909@qq.com>', [email])
	# msg.content_subtype = "html"
	# # 添加附件（可选）添加附件的话，一定要将文件放在一个相对文件夹中，否则会找不到路径，例如static的相对路径已经在settings里面设置，所以可以访问
	# msg.attach_file(r'static/file/Django.doc')


	# # 发送
	# msg.send()
	return JsonResponse(data)

# 修改密码
def change_password(request):
	# 返回链接
	redirect_to=redirect(reverse('home'))
	if request.method =='POST':
		form=ChangePasswordForm(request.POST,user=request.user)
		if form.is_valid():
			user=request.user
			new_password=form.cleaned_data['new_password']
			# 设置新的密码
			user.set_password(new_password)
			user.save()
			# 登出，不需要user，直接request就可以
			auth.logout(request)
			return redirect_to
	else:
		form=ChangePasswordForm()

	context={}
	context['form']=form
	context['page_title']='修改密码'
	context['form_title']='修改密码'
	context['submit_text']='修改'
	context['retrun_back']=redirect_to

	return render(request,'form.html',context)

def forgot_password(request):
	# 返回链接
	redirect_to=redirect(reverse('login'))
	if request.method =='POST':
		form=ForgotPasswordForm(request.POST,request=request)
		if form.is_valid():
			email=form.cleaned_data['email']
			user=User.objects.get(email=email)
			new_password=form.cleaned_data['new_password']
			# 设置新的密码
			user.set_password(new_password)
			user.save()
			return redirect_to
	else:
		form=ForgotPasswordForm()

	context={}
	context['form']=form
	context['page_title']='忘记密码'
	context['form_title']='找回密码'
	context['submit_text']='重置'
	context['retrun_back']=redirect_to

	return render(request,'user/forgot_password.html',context)




 

 


 
