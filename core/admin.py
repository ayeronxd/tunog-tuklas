from django.contrib import admin
from .models import Account, Level, Material, MaterialContent

# Register your models here.
admin.site.register(Account)
admin.site.register(Level)
admin.site.register(Material)
admin.site.register(MaterialContent)
