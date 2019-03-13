from django.contrib import admin
from blog import models

class articleconfig(admin.ModelAdmin):
    list_display = ['title','create_time']

# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.Article,articleconfig)
admin.site.register(models.Blog)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.ArticleToTag)
admin.site.register(models.ArticleDetail)
admin.site.register(models.ArticleUpDown)



