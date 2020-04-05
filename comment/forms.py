from django import forms
from django.contrib.contenttypes.models import ContentType
#对象不存在的错误类型
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	# error_messages={'required':'评论内容不能为空'}设置字段的错误提示信息
	text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),error_messages={'required':'评论内容不能为空'})

	#此字段可以判断用户是直接评论还是回复评论
	reply_comment_id=forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))

	#继承类的对象，需要传递父类以外的参数，必须这样写
	def __init__(self,*args,**kwargs):
		#判断初始化的时候，user对象是否在参数中，避免没有的时候，报错

		if 'user' in kwargs:
			#取出参数，并且赋值，此时参数kwargs就没有了user的值了，取出不放回的意思
			self.user=kwargs.pop('user')
		#继承类的类，必须有此句
		super(CommentForm,self).__init__(*args,**kwargs)

	def clean(self):
		#判断用户是否登录
		if self.user.is_authenticated:
			self.cleaned_data['user']=self.user

		else:
			raise forms.ValidationError('用户未登录')


		#验证评论的对象
		content_type=self.cleaned_data['content_type']
		object_id=self.cleaned_data['object_id']

		try:
			#获取模型的所有对象信息
			model_class=ContentType.objects.get(model=content_type).model_class()
			model_obj=model_class.objects.get(pk=object_id)
			# 将获取的对象传入到cleaned_data数据当中
			self.cleaned_data['content_object']=model_obj
		except ObjectDoesNotExist as e:
			raise forms.ValidationError('评论的对象不存在呢！')
		

		return self.cleaned_data



	def clean_reply_comment_id(self):
		reply_comment_id =self.cleaned_data['reply_comment_id']

		if reply_comment_id < 0:
			raise forms.ValidationError('回复出错')
		elif reply_comment_id ==0:
			self.cleaned_data['parent']=None
		# 如果存在，则返回parent对象
		elif Comment.objects.filter(pk=reply_comment_id).exists():
			self.cleaned_data['parent']=Comment.objects.get(pk=reply_comment_id)
		else:
			raise forms.ValidationError('回复出错')

		return reply_comment_id

