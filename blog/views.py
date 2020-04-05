from django.shortcuts import render_to_response,get_object_or_404,render
from .models import Blog,BlogType
from django.core.paginator import Paginator
#引用设置里面的参数
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
#导入form类
from comment.forms import CommentForm

from read_number.utils import read_num_once_read
from comment.models import Comment


#获取设置的数据
each_page_num=settings.EACH_PAGE_BLOGS_NUMBER

#公用的代码
def get_blog_list_common_data(request,blogs):
	#通过url传递的参数，获取page的参数，调用的字典的get方法，当没有的page的时候，返回默认的参数1
	page_num=request.GET.get("page",1)
	#获取分页器,每页10条数据
	paginator=Paginator(blogs,each_page_num)
	#获取指定的页
	page_of_blogs=paginator.get_page(page_num)#此方法返回的具体的某一页，如果用户输入的参数超出页码的范围，则会自动返回到第一页，如果是非数字，例如page=a也会返回第一页。
	#获取当前的页
	current_page_num = page_of_blogs.number
	#页面范围,当前页的前二页和后二页，最小页（当前页-2）需要和1比较取最大值，最大页（当前页+2）和总页数比较取最小值
	page_range=list(range(max(current_page_num-2,1),current_page_num))+list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
	#加上省略号的标记,当最前页（当前页-2）大于3页的时候，
	if page_range[0]-1>=2:
		#在0的位置插入...标记符
		page_range.insert(0,'...')

	if paginator.num_pages - page_range[-1] >=2:
		print("满足最后加的条件")
		page_range.append('...')

	#加上首页和尾页

	if page_range[0] !=1:
		page_range.insert(0,1)

	#如果最后的页码数不是尾页，则添加尾页
	if page_range[-1] !=paginator.num_pages:
		page_range.append(paginator.num_pages)

	#获取博客分类对应的博客数量.通过annotate拓展，添加blog_count字段，用count统计，添加的依据来自Blog对象数量，用小写的blog
	blog_types=BlogType.objects.annotate(blog_count=Count('blog'))
	'''blog_types=BlogType.objects.all()
	blog_types_list=[]
	#for循环中blog——type是一个实例，blog_type.blog_count是将属性赋予实例对象，然后将对象添加到列表当中去
	for blog_type in blog_types:
		#将对象进行赋值
		blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()
		#类型对象添加到列表中
		blog_types_list.append(blog_type)
	'''
	#获取日期分类对应的博客数量
	blog_dates=Blog.objects.dates("create_time",'day',order="ASC")
	blog_dates_dict={}
	for blog_date in blog_dates:
		blog_count=Blog.objects.filter(create_time__month=blog_date.month,create_time__day=blog_date.day).count()

		blog_dates_dict[blog_date]=blog_count
		
	context={}
	context['blogs']=page_of_blogs.object_list
	context['page_of_blogs']=page_of_blogs
	context['page_range']=page_range
	context['blog_types']=blog_types
	#获取时间分类对象，通过字段，类型，排序获取
	context['blog_dates']=blog_dates_dict

	#返回字典对象
	return context

def blog_list(request):
	
	#获取全部的列表
	blogs=Blog.objects.all()

	context=get_blog_list_common_data(request,blogs)
	
	return render(request,'blog_list.html',context)


def blog_detail(request,blog_pk):
	blog=get_object_or_404(Blog,pk=blog_pk)
	#调用计数应用read_number中的utils的方法
	read_num_cookie_key=read_num_once_read(request,blog)
	#通过单一的实例对象获取ContentType对象
	#blog_content_type=ContentType.objects.get_for_model(blog)

	#初始加载的时候只显示顶级评论，parent=None既是没有父级
	#comments=Comment.objects.filter(content_type=blog_content_type,object_id=blog_pk,parent=None)


	context={}
	context['blog']=blog
	#根据创建的时间，筛选时间大于__gt当前博客的博客，取集合的最后一个就是上一篇
	context['previous_blog']=Blog.objects.filter(last_uptadaed_time__gt=blog.last_uptadaed_time).last()
	#根据创建的时间，筛选时间小于__lt当前博客的博客，取集合的第一个就是下一篇
	context['next_blog']=Blog.objects.filter(last_uptadaed_time__lt=blog.last_uptadaed_time).first()
	# 将评论内容返回到前端页面,设置数据的排序方式为倒序
	#context['comments']=comments.order_by('-comment_time')

	# #创建一个字典，用来保存默认的数据
	# data={}
	# #根据字段要求，blog_content_type.model的结果是字符类型
	# data['content_type'] = blog_content_type.model
	# data['object_id'] = blog_pk
	# #初始的回复id为0，表示直接评论，不是回复
	# data['reply_comment_id']=0

	# #初始化一个comment_form对象，将字段的初始化数据传递进去，initial=data将隐藏的对象传递进去，否则找不到评论对象，将会报错
	# context['comment_form']=CommentForm(initial=data)
	#定义一个返回的对象
	response=render(request,'blog_detail.html',context)
	#将返回的对象中添加一个cookie，max_age=60设置cookie的有效期为60秒，单位为秒，expires=datetime(2020.1.13)设置一个截止的日期，当日期到了的时候则会失效，和前面的max——age是冲突的，设置以后max——age无效
	#response.set_cookie('blog_%s_is_read'%blog_pk,'ture',max_age=60,expires=datetime(2020.1.13))
	response.set_cookie(read_num_cookie_key,'ture',max_age=60)
	return response

def blogs_with_type(request,blogs_with_type):
	#获取类型
	blog_type=get_object_or_404(BlogType,pk=blogs_with_type)
	#获取全部的列表
	blogs=Blog.objects.filter(blog_type=blog_type)
	#通过调用通用的函数，返回一个字典对象
	context=get_blog_list_common_data(request,blogs)
	context['blog_type']=blog_type.type_name

	
	return render(request,'blogs_with_type.html',context)



def blogs_with_date(request,month,day):
	
	#获取全部的列表
	blogs=Blog.objects.filter(create_time__month=month,create_time__day=day)
	
	#通过调用通用的函数，返回一个字典对象
	context=get_blog_list_common_data(request,blogs)
	context['blogs_with_date']='%s月%s日'%(month,day)

	return render(request,'blogs_with_date.html',context)

