from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'status')
    search_fields = ('number',)
    empty_value_display = '-пусто-'


admin.site.register(Task, TaskAdmin)

