from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Module)
admin.site.register(Student)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    exclude = ('can_start',)

admin.site.register(Professor)
admin.site.register(Question)
