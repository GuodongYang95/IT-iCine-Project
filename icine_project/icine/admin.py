
from django.contrib import admin
from icine.models import Category, Page
from icine.models import UserProfile
# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    
admin.site.register(Page, PageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)

admin.site.register(UserProfile)
