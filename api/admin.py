from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Income)
admin.site.register(Waste)
admin.site.register(Category)