from django.contrib import admin

# Register your models here.
from cdn.models import WASHU,YSTEN


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contentid','c_time') #列出显示的字段
    list_filter = ['c_time'] #添加过滤器
    list_per_page = 15
    search_fields = ('name','contentid')#添加搜索
    

admin.site.register(WASHU,AuthorAdmin)
admin.site.register(YSTEN,AuthorAdmin)
