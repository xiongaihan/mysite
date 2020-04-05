from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
#因为第三方模型已经注册，所以可以直接饮用，导入富文本编辑字段
#from ckeditor.fields import RichTextField
#因为第三方模型已经注册，所以可以直接饮用，导入可以上传图片的富文本编辑字段
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from read_number.models import ReadNumExpandMethod,ReadDetail



# Create your models here.
class BlogType(models.Model):
	type_name=models.CharField(max_length=30,verbose_name='博客分类')


	#此方法使得显示对象的时候，显示对象的名称
	def __str__(self):
		return self.type_name


#继承了计数应用的类，可以使用父类的方法
class Blog(models.Model,ReadNumExpandMethod):
	title=models.CharField(verbose_name='标题',max_length=50)
	blog_type=models.ForeignKey(BlogType,on_delete=models.CASCADE,verbose_name='博客分类')
	#content=RichTextField()
	content=RichTextUploadingField()
	#添加数字字段
	#read_num=models.IntegerField(default=0)
	author=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
	#添加反向关系，类似主表关联从表
	read_details=GenericRelation(ReadDetail)
	create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建日期')
	last_uptadaed_time=models.DateTimeField(auto_now=True,verbose_name='更新日期')

	# 獲取email
	def get_email(self):
		return self.author.email
	
	# 有二個參數reverse('blog_datail',kwargs={'blog_pk':comment.content_object.pk})反向解析當前的url，kwargs={'blog_pk':取決于url設置的關鍵字，不是隨便起的
	def get_url(self):
		return reverse('blog_detail',kwargs={'blog_pk':self.pk})
		

	#此方法使得显示博客对象的时候，只是显示博客的标题

	def __str__(self):
		return "<Blog:%s>"%self.title

	#根据文章的更新时间进行倒序排列
	class Meta:
		ordering=['-last_uptadaed_time']

