from django.contrib import admin
from .models import CustomUser
# Register your models here.
from django.contrib.admin import DateFieldListFilter


# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined')
    search_fields = ['username', 'full_name']
    list_filter = (('date_joined', DateFieldListFilter),)
