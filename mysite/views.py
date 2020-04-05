import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
#引入验证和登录的方法
from django.contrib import auth
#引入缓存对象
from django.core.cache import cache
from blog.models import Blog
from read_number.utils import get_before_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
#导入用户对象
from django.contrib.auth.models import User



def get_week_hot_blogs():
	today=timezone.now().date()
	date=today-datetime.timedelta(days=7)
	#筛选博客对象，通过关联对象的日期筛选，当时间小于今天大于等于前七天的时间段，values主要是添加关键字，将对象返回一个个的字典对象，其实不用values也可以，只是不能使用'id','title'关键字访问，annotate将对象聚合分类
	#Sum('read_details__read_num'将同类的对象的此关键词相加
	blogs=Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date).values('id','title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')

	return blogs[:7]


def home(request):
	context={}
	blog_content_type=ContentType.objects.get_for_model(Blog)
	dates,read_nums=get_before_seven_days_read_data(blog_content_type)
	today_hot_data=get_today_hot_data(blog_content_type)
	yesterday_hot_data=get_yesterday_hot_data(blog_content_type)

	#获取7天的热门数据，通过缓存获取
	week_hot_blogs=cache.get('week_hot_blogs')
	#如果没有缓存，或者缓存过期，则缓存对象为None，执行if语句

	if week_hot_blogs is None:
		week_hot_blogs=get_week_hot_blogs()
		#设置缓存数据，'week_hot_blogs'表示缓存的名称，week_hot_blogs表示缓存数据，20缓存有效期20s
		cache.set('week_hot_blogs',week_hot_blogs,20)
		print("calc")
	else:
		print('use cache')

	context['read_nums']=read_nums
	context['dates']=dates
	context['today_hot_data']=today_hot_data
	context['yesterday_hot_data']=yesterday_hot_data
	context['week_hot_blogs']=week_hot_blogs
	return render(request,'home.html',context)



