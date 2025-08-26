# import form class from django
from django import forms
from captcha.fields import CaptchaField
from cmsapp.models import *
from .models import *





# this central fucntion use for upload multiplefile. set all view.py want use it. 		

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True		

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
# this fucntion use for upload multiplefile. set all view.py want use it. 


class SerVerMaintenForm(forms.ModelForm):
	# specify the name of model to use
	#captcha = CaptchaField()
	img_case = MultipleFileField(label = 'เพิ่มภาพ',required=True) 
	class Meta:
		model = SerVerMainten
		fields = "__all__"

		widgets = { 
			'server_name':forms.Select(attrs={'class':'form-control','required':'True',}),
			'case_diag':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'resolve_Methode': forms.TextInput(attrs={'class':'form-control','required':'True',}),		
			'user':forms.HiddenInput(),  #auto input field when login 			

		}
		labels = {
			'server_name':'ชื่อเครื่องเซิร์ฟเวอร์',
			'case_diag':'สาเหตุขัดข้อง',
			'resolve_Methode':'วิธีการแก้ปัญหา',			
							
			'user':'ผู้ตรวจ', #'reporter':'ผู้เขียน', เพื่มอัตโนมัติ 'reporter':forms.HiddenInput(),
		}


class addSerVerForm(forms.ModelForm):
	# specify the name of model to use
	#captcha = CaptchaField()
	img_server = MultipleFileField(label = 'เพิ่มภาพ',required=True) 
	class Meta:
		model = Server
		fields = "__all__"

		widgets = { 
			'server_procument_id':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'server_service_name':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'server_brand_name':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'server_model_name':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'server_year_register':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'False',}),	
			'server_domain_name':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'server_ip':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'server_user':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'server_password':forms.TextInput(attrs={'class':'form-control','required':'True',}),

		}
		labels = {
			'server_procument_id':'เลขครุภัณฑ์คอมพิวเตอร์',
			'server_service_name':'ชื่อบริการเครื่องเซิร์ฟเวอร์',
			'server_brand_name':'ยี่ห้อเครื่องเซิร์ฟเวอร์',
			'server_model_name':'รุ่นเครื่องเซิร์ฟเวอร์',	
			'server_year_register':'ปีที่รับ',			
			'server_domain_name':'ชื่อโดเมนเนม',			
			'server_ip':'IP address',			
			'server_user':'User',			
			'server_password':'Password',						
			
		}