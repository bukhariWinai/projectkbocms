from django.contrib import admin
from .models import *
from cmsapp.models import *

# Register your models here.
admin.site.register(Trainee)
admin.site.register(School)
admin.site.register(Degree)
admin.site.register(TitleName)
admin.site.register(ImagesCloud)
admin.site.register(DailyWorkReport)



