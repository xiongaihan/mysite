from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '简介'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display=('username','nickname','email','is_staff','is_active','is_superuser')

    # 自定义显示字段，每一个user对应一个profile对象，profile对象有nickname属性
    def nickname(self,obj):
    	return obj.profile.nickname

    # 显示名称。可以覆盖vobse——name的设置
    nickname.short_description='新昵称'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display =("user","nickname")