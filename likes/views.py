from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount,LikeRecord



def errorResponse(code,message):
	data={}
	data['status']='ERROR'
	data['code']=code
	data['message']=message
	return JsonResponse(data)


def successResponse(liked_num):
	data={}
	data['status']='SUCCESS'
	data['liked_num']=liked_num
	return JsonResponse(data)




def like_change(request):
	# 获取数据
	user=request.user

	if not user.is_authenticated:
		return errorResponse(400,'没有登录，请登录')
	#获取类型的字符串，
	content_type_str=request.GET.get('content_type')
	
	object_id=int(request.GET.get('object_id'))
	is_like=request.GET.get('is_like')

	try:
		#转换为content_type类型
		content_type=ContentType.objects.get(model=content_type_str)
		#获取所有的对象
		model_class=content_type.model_class()
		#获取点赞对象
		model_obj=model_class.objects.get(pk=object_id)
	except ObjectDoesNotExist as e:
		return errorResponse(400,'评论的对象不存在')


	#处理数据
	if is_like=='true':
		# 要点赞
		like_record,created=LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
		# 如果对象是新创建的
		if created:
			#未点赞过，进行点赞
			like_count,created=LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
			# 无论是否是创建的对象，都会将属性like_num+1
			like_count.liked_num+=1
			like_count.save()
			# 返回点赞数量
			return successResponse(like_count.liked_num)
		else:
			#已经点赞过，不能重复点赞
			return errorResponse(402,'已经点赞过，不能重复点赞')
	else:
		# 取消点赞
		#先判断是否存在
		if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
			#有点赞过，取消点赞
			like_record=LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
			like_record.delete()
			#点赞的总数-1
			#获取或者创建点赞总数对象
			like_count,created=LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
			if not created:
				like_count.liked_num-=1
				if like_count.liked_num<0:
					like_count.liked_num=0
				like_count.save()
				# 返回点赞数量
				return successResponse(like_count.liked_num)
			else:
				return errorResponse(403,'数据错误')

		else:
			# 没有点赞过，不能取消
			return errorResponse(404,'没有点赞过，不能取消')

