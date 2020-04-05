from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	# required=True此字段不能为空，默认是不为空，False为可以为空
	username_or_email=forms.CharField(label='用户名或邮箱',required=False,widget=forms.TextInput( attrs={'class':'form-control','placeholder':'请输入用户名或者邮箱'}))
	password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))


	def clean(self):
		# 调用此方法的时候，返回了前端的信息
		username_or_email=self.cleaned_data['username_or_email']
		password=self.cleaned_data['password']

		#账号验证，可以不用request
		user=auth.authenticate(username=username_or_email,password=password)

		# 直接用户名验证不通过，用邮箱验证
		if user is None:
			print('开始验证邮箱')
			# 如果邮箱存在,当数量为1的时候才可以继续，如果多个以后有同一个邮箱，将会导致异常
			if User.objects.filter(email=username_or_email).count() == 1:
				print('邮箱存在')
				# get方法只能返回一个对象，如果返回多个就会报错
				username=User.objects.get(email=username_or_email).username
				#账号验证，可以不用request
				user=auth.authenticate(username=username,password=password)

				if not user is None:
					self.cleaned_data['user']=user
					return self.cleaned_data
			#验证不通过，返回错误信息
			raise forms.ValidationError('用户名或者密码不正确！！！')
		else:
			#验证通过，有此用户，将用户信息，添加到cleaned_data字典中，以便使用
			self.cleaned_data['user']=user
		return self.cleaned_data


class RegForm(forms.Form):
	
	username=forms.CharField(label='用户名',
							max_length=30,
							min_length=3,
							widget=forms.TextInput( attrs={'class':'form-control','placeholder':'请输入3-30位的用户名'}))
	
	email=forms.CharField(label='邮箱',
							widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))

	verification_code=forms.CharField(label='验证码',
							required=False,
							widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入验证码'}))

	password=forms.CharField(label='密码',
							min_length=6,
							widget=forms.PasswordInput( attrs={'class':'form-control','placeholder':'请输入密码'}))
	
	password_again=forms.CharField(label='确认密码',
							min_length=6,
							widget=forms.PasswordInput( attrs={'class':'form-control','placeholder':'请再输入一次密码'}))
	


	#继承类的对象，需要传递父类以外的参数，必须这样写
	def __init__(self,*args,**kwargs):
		#判断初始化的时候，user对象是否在参数中，避免没有的时候，报错

		if 'request' in kwargs:
			#取出参数，并且赋值，此时参数kwargs就没有了user的值了，取出不放回的意思
			self.request=kwargs.pop('request')
		#继承类的类，必须有此句
		super(RegForm,self).__init__(*args,**kwargs)


	def clean(self):
		# 获取产生的code
		random_code=self.cleaned_data.get('email','')
		print('注册获取的邮箱key:'+random_code)
		code=self.request.session.get(random_code,'')
		print('注册的时候随机产生的code：'+code)

		verification_code=self.cleaned_data.get('verification_code','')

		print('用户填写的code：'+verification_code)
		if not ((verification_code != '') & (verification_code==code)):

			raise forms.ValidationError('验证码不正确')

		print('验证通过')
		return self.cleaned_data
	
	def clean_username(self):
		username=self.cleaned_data['username']
		#判断用户名是否存在
		if User.objects.filter(username=username).exists():
			#如果用户名存在，返回错误信息
			raise forms.ValidationError('用户名已使用')

		return username


	def clean_email(self):
		email=self.cleaned_data['email']
		#判断用户名是否存在
		if User.objects.filter(email=email).exists():
			#如果用户名存在，返回错误信息
			raise forms.ValidationError('邮箱已注册')

		return email

	def clean_password_again(self):
		password=self.cleaned_data['password']
		password_again=self.cleaned_data['password_again']

		if password !=password_again :
			raise forms.ValidationError('二次输入的密码不一致')

		return password_again

class ChangeNicknameForm(forms.Form):

	nickname_new=forms.CharField(label='新的昵称',max_length=30,widget=forms.TextInput( attrs={'class':'form-control','placeholder':'请输入新的昵称'}))


	#继承类的对象，需要传递父类以外的参数，必须这样写
	def __init__(self,*args,**kwargs):
		#判断初始化的时候，user对象是否在参数中，避免没有的时候，报错

		if 'user' in kwargs:
			#取出参数，并且赋值，此时参数kwargs就没有了user的值了，取出不放回的意思
			self.user=kwargs.pop('user')
		#继承类的类，必须有此句
		super(ChangeNicknameForm,self).__init__(*args,**kwargs)

	def clean(self):
		#判断用户是否登录
		if self.user.is_authenticated:
			self.cleaned_data['user']=self.user

		else:
			raise forms.ValidationError('用户未登录')

		# 返回整个数据
		return self.cleaned_data

	def clean_nickname_new(self):
		# 获取传递的昵称，将前后空格去掉
		nickname_new=self.cleaned_data['nickname_new'].strip()

		if nickname_new =='':
			raise forms.ValidationError('新的昵称不能为空')
		# 返回验证的字段
		return nickname_new



class BindEmailForm(forms.Form):
	email=forms.CharField(label='邮箱',
							widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
	
	verification_code=forms.CharField(label='验证码',
							required=False,
							widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入验证码'}))


	#继承类的对象，需要传递父类以外的参数，必须这样写
	def __init__(self,*args,**kwargs):
		#判断初始化的时候，user对象是否在参数中，避免没有的时候，报错

		if 'request' in kwargs:
			#取出参数，并且赋值，此时参数kwargs就没有了user的值了，取出不放回的意思
			self.request=kwargs.pop('request')
		#继承类的类，必须有此句
		super(BindEmailForm,self).__init__(*args,**kwargs)

	def clean(self):
		#判断用户是否登录
		if self.request.user.is_authenticated:
			self.cleaned_data['user']=self.request.user

		else:
			raise forms.ValidationError('用户未登录')

		# 判断用户是否绑定邮箱
		if self.request.user.email!='':
			print('用戶已經綁定')
			raise forms.ValidationError('用户已经绑定邮箱')


		# 判断验证码是否正确
		# 获取随机产生的code，存储在session当中，所填的email就是key

		code=self.request.session.get(self.cleaned_data['email'],'')
		print('随机产生的'+code)

		verification_code=self.cleaned_data.get('verification_code','')
		print('自己填的'+verification_code)
		print(verification_code==code)
		print(verification_code != '')
		print('@@@@@@@@@@@@')
		print((verification_code != '') & (verification_code==code))
		print(not ((verification_code != '') & (verification_code==code)))
		print('***********')
		if not ((verification_code != '') & (verification_code==code)):

			raise forms.ValidationError('验证码不正确')

		print('验证通过')
		return self.cleaned_data
	
	# 验证字段的时候不要和主要的验证冲突，字段验证不通过以后，将不会返回验证的字段，此时再获取cleaned_data就会报错keyerror
	# def clean_email(self):
	# 	email=self.cleaned_data['email']

	# 	if User.objects.filter(email=email).exists():
	# 		raise forms.ValidationError('邮箱已经被绑定')

	# 	return email


	# 验证字段的时候不要和主要的验证冲突，字段验证不通过以后，将不会返回验证的字段，此时再获取cleaned_data就会报错keyerror
	def clean_verification_code(self):
		verification_code=self.cleaned_data['verification_code']
		if verification_code == '':
			print('验证码为空')
			raise forms.ValidationError('字段验证-不能为空')

		return verification_code



	


class ChangePasswordForm(forms.Form):
	old_password=forms.CharField(label='旧的密码',
			widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请输入旧的密码'}
			))

	new_password=forms.CharField(label='新密码',
			widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请输入新的密码'}
			))
	new_password_again=forms.CharField(label='确认密码',
			widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请再次输入新的密码'}
			))

	#继承类的对象，需要传递父类以外的参数，必须这样写
	def __init__(self,*args,**kwargs):
		#判断初始化的时候，user对象是否在参数中，避免没有的时候，报错

		if 'user' in kwargs:
			#取出参数，并且赋值，此时参数kwargs就没有了user的值了，取出不放回的意思
			self.user=kwargs.pop('user')
		#继承类的类，必须有此句
		super(ChangePasswordForm,self).__init__(*args,**kwargs)

	def clean(self):
		# 验证新的密码是否一致
		new_password=self.cleaned_data.get('new_password','')
		new_password_again=self.cleaned_data.get('new_password_again','')

		if new_password_again != new_password or new_password == '':
			raise forms.ValidationError('二次输入的密码不一致')


		return self.cleaned_data


	def clean_old_password(self):
		# 验证旧的密码是否正确

		old_password=self.cleaned_data.get('old_password','')
		# 验证当前对象的user的密码是否正确self.user.check_password(old_password)，密码正确返回true，否则false
		if not self.user.check_password(old_password):
			raise forms.ValidationError('密码不正确')
		return old_password


class ForgotPasswordForm(forms.Form):
	email=forms.CharField(label='邮箱',
			widget=forms.EmailInput(
			attrs={'class':'form-control','placeholder':'请输入邮箱'}))

	verification_code=forms.CharField(label='验证码',
			required=False,
			widget=forms.TextInput(
			attrs={'class':'form-control','placeholder':'请输入验证码'}))


	new_password=forms.CharField(label='新密码',
			widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请输入新的密码'}
			))
	new_password_again=forms.CharField(label='再次确认密码',
			widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请再次输入新的密码'}
			))


	#继承类的对象，需要传递父类以外的参数，必须这样写
	def __init__(self,*args,**kwargs):
		#判断初始化的时候，user对象是否在参数中，避免没有的时候，报错

		if 'request' in kwargs:
			#取出参数，并且赋值，此时参数kwargs就没有了user的值了，取出不放回的意思
			self.request=kwargs.pop('request')
		#继承类的类，必须有此句
		super(ForgotPasswordForm,self).__init__(*args,**kwargs)

	def clean_email(self):
		# 获取邮箱进行验证
		email=self.cleaned_data.get('email','')
		if not User.objects.filter(email=email).count() == 1:
			raise forms.ValidationError('邮箱未绑定')
		return email

	

	def clean_verification_code(self):
		# 获取产生的code
		random_code=self.cleaned_data.get('email','')
		print('忘记密码获取的邮箱key:'+random_code)
		print(random_code)
		print(type(random_code))
		code=self.request.session.get(random_code,'')
		print('忘记密码随机产生的code：'+code)

		verification_code=self.cleaned_data.get('verification_code','')

		print('用户填写的code：'+verification_code)
		if not ((verification_code != '') & (verification_code==code)):

			raise forms.ValidationError('验证码不正确')

		print('验证通过')

		return verification_code

	def clean_new_password_again(self):
		new_password=self.cleaned_data['new_password']
		new_password_again=self.cleaned_data['new_password_again']

		if new_password !=new_password_again or new_password_again == '':
			raise forms.ValidationError('二次输入的密码不一致')

		return new_password_again
