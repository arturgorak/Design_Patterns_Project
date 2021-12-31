from django.contrib import admin
from .models import *


class ScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam', 'total', 'grade', 'comment']


class AllocationAdmin(admin.ModelAdmin):
    list_display = ['teacher', ]





admin.site.register(Student)
admin.site.register(Session)
admin.site.register(User)
admin.site.register(Class)
admin.site.register(Grade)
admin.site.register(Teacher)
admin.site.register(Director)
admin.site.register(Subject)

