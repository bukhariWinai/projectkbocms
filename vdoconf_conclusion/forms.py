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


class VdoconfConclusionForm(forms.ModelForm):
	# specify the name of model to use
	#captcha = CaptchaField()
	img_vdoconf = MultipleFileField(label = 'เพิ่มภาพ',required=True) 
	class Meta:
		model = VdoconfConclusion
		fields = "__all__"

		widgets = { 
			'vdoconfdate':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'False',}),		
			
			'vdoconftitle':forms.TextInput(attrs={'class':'form-control','required':'True',}),		
			'vdoconftitle':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'confDetail':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'link_url_vdo':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'user':forms.HiddenInput(),  #auto input field when login 			

		}
		labels = {
			'vdoconfdate':'วันประชุม',

			'vdoconftitle':'เรื่องการประชุม',
			'confDetail':'สรุปรายละเอียดการประชุม',
			'link_url_vdo':'ลิงค์ VDO',
							
			'user':'ผู้บันทึก', #'reporter':'ผู้เขียน', เพื่มอัตโนมัติ 'reporter':forms.HiddenInput(),
		}


