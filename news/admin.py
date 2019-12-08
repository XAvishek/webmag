from django.contrib import admin
from news.models import Comment, News
# Register your models here.


admin.site.register(News)
admin.site.register(Comment)