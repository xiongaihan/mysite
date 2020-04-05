from django import template
from django.contrib.contenttypes.models import ContentType
# 引用上层的文件夹
from ..models import LikeCount,LikeRecord


register=template.Library()

# 注册模板便签，必须这样写，启用的时候，需要重启服务
@register.simple_tag
def get_like_count(obj):
	content_type =ContentType.objects.get_for_model(obj)
	# 获取点赞总数对象
	like_count,crated=LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)
	return like_count.liked_num

# 注册的时候加上takes_context=True，表示调用这个模板标签的时候，会将模板的数据返回过来，例如模板标签有user对象，可以将user返回到此处使用
@register.simple_tag(takes_context=True)
def get_like_status(context,obj):
	content_type =ContentType.objects.get_for_model(obj)
	user=context['user']
	if not user.is_authenticated:
		return ''
	# 此处不新创建对象，原因是如果创建的话，在未点赞的时候，也会创建点赞记录，并且需要对点赞数量进行判断
	if LikeRecord.objects.filter(content_type=content_type,object_id=obj.pk,user=user).exists():
		return 'active'
	else:
		return ''


@register.simple_tag
def get_content_type(obj):
	content_type =ContentType.objects.get_for_model(obj)
	# 返回字符串类型
	return content_type.model