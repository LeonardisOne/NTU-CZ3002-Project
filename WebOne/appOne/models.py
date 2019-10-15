from django.db import models
from django.urls import reverse
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
    prof_title = UserProfileInfo.user

    def __str__(self):
        return self.prof_title.username


class Module(models.Model):

    module_name = models.CharField(max_length=50)
    coordinator = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (("can_modify_module", "Can create/delete a module"),)#placeholder

    def get_absolute_url(self):
        return reverse('appOne:module_home', args=[str(self.module_name)])

    def __str__(self):
        return self.module_name

class Chapter(models.Model):

    chapter_name = models.CharField(max_length=50,default="")
    chapter_desc = models.CharField(max_length=100)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    can_start = models.BooleanField(default=False, null=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = (("can_publish_chapter", "Can publish a chapter"),
                        ("can_try_qn", "Can try questions in a chapter"))

    def get_absolute_url(self):
        return reverse('appOne:chapter_home', kwargs={'pk': self.module.module_name,
                                        'pq': self.chapter_name})

    def __str__(self):
        return f"{str(self.module)} {self.chapter_name}"

class ChapterTeamManager(models.Manager):
    def create_team(self, chapter, team_name):
        team = self.create(chapter=chapter, team_name=team_name)
        return team

class ChapterTeam(models.Model):
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    team_name = models.CharField(max_length=20)
    room_id = models.CharField(max_length=30)

    objects = ChapterTeamManager()

    def _str_(self):
        return self.team_name

class Student(UserProfileInfo):
    modules_taken = models.ManyToManyField(Module)
    joined_teams = models.ManyToManyField(ChapterTeam)

class Question(models.Model):
    question_number = models.PositiveIntegerField()
    question_name = models.CharField(max_length=500) #Question statement
    question_optionA = models.CharField(max_length=100)
    question_optionB = models.CharField(max_length=100)
    question_optionC = models.CharField(max_length=100)
    question_optionD = models.CharField(max_length=100)

    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)

    class Meta:
        permissions = (("can_modify_question","Can create/delete a question"),)

    def __str__(self):
        return f"{str(self.chapter)} {self.question_name}"

class Solution(models.Model):

    solution_name = models.CharField(max_length=50) #solution_name is the solution to certain question.
    solution_answer = models.CharField(max_length=50)
    solution_explanation = models.CharField(max_length=50)

    question = models.ForeignKey('Question',on_delete=models.CASCADE)
    class Meta:
        permissions = (("can_modify_solution","Can create/delete a solution"),)

    def __str__(self):
        return self.solution_name
