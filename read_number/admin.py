from django.contrib import admin
from .models import ReadNum,ReadDetail

# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
	list_display=("id","read_num","content_type","object_id","content_object")



@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
	list_display=("id","read_num","date","content_type","object_id","content_object")