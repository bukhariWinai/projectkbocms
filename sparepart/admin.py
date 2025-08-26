from django.contrib import admin
from .models import *
from cmsapp.models import *

admin.site.register(ItemsRepairOrderParts)
admin.site.register(PartRepairImage)
admin.site.register(PartsStock)
admin.site.register(PartImage)
# admin.site.register(PartsName)

# Register your models here.
