from django import template
from django.contrib.contenttypes.models import ContentType
# 引用上层的文件夹
from ..models import Comment
from ..forms import CommentForm


register=template.Library()

# 注册模板便签，必须这样写，启用的时候，需要重启服务
@register.simple_tag
def get_comment_count(obj):
	content_type =ContentType.objects.get_for_model(obj)
	# 获取评论数
	count=Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()
	# 返回评论数
	return count

# 注册模板便签，必须这样写，启用的时候，需要重启服务
@register.simple_tag
def get_comment_form(obj):

	content_type =ContentType.objects.get_for_model(obj)
	#创建一个字典，用来保存默认的数据
	data={}
	#根据字段要求，blog_content_type.model的结果是字符类型
	data['content_type'] = content_type.model
	data['object_id'] = obj.pk
	#初始的回复id为0，表示直接评论，不是回复
	data['reply_comment_id']=0

	#初始化一个comment_form对象，将字段的初始化数据传递进去，initial=data将隐藏的对象传递进去，否则找不到评论对象，将会报错
	form=CommentForm(initial=data)

	return form

@register.simple_tag
def get_comment_list(obj):
	content_type =ContentType.objects.get_for_model(obj)
	#初始加载的时候只显示顶级评论，parent=None既是没有父级
	comments=Comment.objects.filter(content_type=content_type,object_id=obj.pk,parent=None)

	return comments.order_by('-comment_time')