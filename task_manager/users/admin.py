from django.contrib import admin
from .models import User
# Register your models here.
from django.contrib.admin import DateFieldListFilter


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'created_at')
    search_fields = ['nickname', 'full_name']
    list_filter = (('created_at', DateFieldListFilter),)
