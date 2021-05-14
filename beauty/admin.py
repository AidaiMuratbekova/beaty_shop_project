from django.contrib import admin

from .models import *




# @admin.register(Product)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [ProductImageInline, ]

admin.site.register(Product)
admin.site.register(Category)