# import form class from django
from django import forms
from captcha.fields import CaptchaField

# import GeeksModel from models.py
#from django.forms.widgets import DateTimeWidget
from .models import *

# create a ModelForm
class NewsForm(forms.ModelForm):
	# specify the name of model to use
	captcha = CaptchaField()
	class Meta:
		model = News
		fields = "__all__"

	

		widgets = { 
			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'post':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			#'image1':forms.ImageField(attrs={'class':'form-control',}),
			'reporter':forms.Select(attrs={'class':'form-control','required':'True',}),
			'section':forms.Select(attrs={'class':'form-control','required':'True',}),
			'category':forms.Select(attrs={'class':'form-control','required':'True',}),
			'slug':forms.TextInput(attrs={'class':'form-control',}),

		}
		labels = {
			'date':'วันที่',
			'title':'หัวข้อข่าว',
			'post':'เนื้อหาข่าว',
			'title_photo':'ภาพพาดหัวข่าว',
			'photo1':'ภาพประกอบ1',
			'photo2':'ภาพประกอบ2',
			'reporter':'ผู้เขียน',
			'section':'กลุ่มงาน',
			'category':'หมวดข่าว',
			'slug':'ลิงค์ข่าว',
			

		}
