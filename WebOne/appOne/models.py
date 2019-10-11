from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # additional
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Professor(UserProfileInfo):
    prof_title = models.CharField(max_length=30)

class Module(models.Model):

    module_name = models.CharField(max_length=50)
    coordinator = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (("can_modify_module", "Can create/delete a module"),)#placeholder

    def __str__(self):
        return self.module_name

class Student(UserProfileInfo):
    modules_taken = models.ManyToManyField(Module)

class Chapter(models.Model):

    chapter_name = models.CharField(max_length=50)
    chapter_desc = models.CharField(max_length=100, default= 'Description')
    module = models.ForeignKey('Module', on_delete=models.CASCADE)

    class Meta:
        permissions = (("can_modify_chapter", "Can create/delete a chapter"),)#placeholder

    def __str__(self):
        return self.chapter_name