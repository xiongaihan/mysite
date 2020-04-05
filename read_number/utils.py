import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail




def read_num_once_read(request,obj):
	#通过传进的对象，获取模型
	ct=ContentType.objects.get_for_model(obj)
	#创建一个字符串，ct.model获取模型的名称，例如获取blog模型的名称，obj。pk是传入对象的主键
	key='%s_%s_read'%(ct.model,obj.pk)
	'''判断语句，如果在所有的cookie字典中能够找到blog——id的对象，
	则会返回对应的value值，否则会返回none，none对应false，加not取反，
	如果没有阅读就会执行下面的语句'''
	if not request.COOKIES.get(key):
		#根据条件判断，对象是否存在，如果存在则返回对象，如果不存在则创建一个新对象，created当对象存在返回true，不存在返回false
		readnum,created=ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)

		#总的阅读数计数+1
		readnum.read_num+=1
		readnum.save()

		#创建当天日期对象
		date=timezone.now().date()
		#当天阅读数+1
		readDetaile,created=ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
		readDetaile.read_num+=1
		readDetaile.save()

	#返回key值
	return key


def get_before_seven_days_read_data(content_type):
	#获取当天的日期
	today=timezone.now().date()
	read_nums=[]
	dates=[]
	for i in range(7,0,-1):
		#获取i天前的日期，通过今天的日期，进行差量计算。
		date=today-datetime.timedelta(days=i)
		#将日期按固定的格式返回。
		dates.append(date.strftime('%m/%d'))
		#通过传入的模型类型，时间，筛选符合的readdetail对象，返回一个结果集，类型数据库查询的时候，只用二个条件查询
		read_details=ReadDetail.objects.filter(content_type=content_type,date=date)
		#返回一个聚合函数的集合
		result=read_details.aggregate(read_num_sum=Sum('read_num'))
		#参数中如果结果为前面的结果None则返回后面的0
		read_nums.append(result['read_num_sum'] or 0)

	return dates,read_nums


#获取今日的热门博客数据
def get_today_hot_data(content_type):
	#获取今天的日期
	today=timezone.now().date()
	#筛选符合条件的对象，并且按阅读的数量排序
	read_details=ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
	#返回前七个的对象
	return read_details[:7]




#获取昨日的热门博客数据
def get_yesterday_hot_data(content_type):
	#获取今天的日期
	today=timezone.now().date()
	#获取昨日的日期对象
	yesterday=today-datetime.timedelta(days=1)
	#筛选符合条件的对象，并且按阅读的数量排序
	read_details=ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
	#返回前七个的对象
	return read_details[:7]

