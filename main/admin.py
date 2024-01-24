from django.contrib import admin
from . import models
# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_tag')


admin.site.register(models.Banners, BannerAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')


admin.site.register(models.Service, ServiceAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(models.Page, PageAdmin)
