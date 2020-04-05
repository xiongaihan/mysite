from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	# 一一对应的关系，一个user对应一个user
	user=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='用户')
	nickname=models.CharField(max_length=20,verbose_name='昵称')


	def __str__(self):
		return '<Profile:%s for %s>'%(self.nickname,self.user.username)



def get_nickname(self):

	if Profile.objects.filter(user=self).exists():
		profile=Profile.objects.get(user=self)
		return profile.nickname

	else:
		return ''


def get_nickname_or_username(self):

	if Profile.objects.filter(user=self).exists():
		profile=Profile.objects.get(user=self)
		return profile.nickname

	else:
		return self.username

def has_nickname(self):
	return Profile.objects.filter(user=self).exists()
# 类的动态绑定，当user实例对象有了以后，将会有这个属性
User.get_nickname=get_nickname
User.has_nickname=has_nickname
User.get_nickname_or_username=get_nickname_or_username
