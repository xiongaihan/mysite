from django.contrib import admin
from .models import LikeCount,LikeRecord

# Register your models here.
@admin.register(LikeCount)
class LikesAdmin(admin.ModelAdmin):
	list_display=("id","content_type","object_id","content_object","liked_num")



@admin.register(LikeRecord)
class LikesAdmin(admin.ModelAdmin):
	list_display=("id","content_type","object_id","content_object","user","liked_time")