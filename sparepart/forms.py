# import form class from django
from django import forms
from captcha.fields import CaptchaField
from cmsapp.models import *
from .models import *
from django.forms import formset_factory

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

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs.setdefault('class', 'form-control')

        # ควบคุมการทำงานของ Forms.py

class AddPartsForm(forms.ModelForm):
	
	#captcha = CaptchaField()
	img_case = MultipleFileField(label = 'เพิ่มภาพ',required=True) 
	class Meta:
		model = ItemsRepairOrderParts
		fields = "__all__"


class AddPartsCatForm(forms.ModelForm):
	# specify the name of model to use
	#captcha = CaptchaField()
	#img_server = MultipleFileField(label = 'เพิ่มภาพ',required=True) 
	class Meta:
		model = Parts_Category
		fields = "__all__"
		widgets = { 
			'parts_cat_name':forms.TextInput(
				attrs={'class':'form-control',
				'required':'True',
				'placeholder':'เช่น Ram , Hdd , SSd เป็นต้น'
				}),			

		}
		labels = {
			'parts_cat_name':'ชื่อชนิดวัสดุคอมพิวเตอร์',
			}
			

class AddPartsSubForm(forms.ModelForm):
	# specify the name of model to use
	#captcha = CaptchaField()
	#img_server = MultipleFileField(label = 'เพิ่มภาพ',required=True) 
	class Meta:
		model = PartsSubCatName
		fields = "__all__"

		widgets = { 
			'parts_cat_name':forms.Select(
				attrs={'class':'form-control',
				'required':'True',
				
				}),
			'parts_sub_name':forms.TextInput(
				attrs={'class':'form-control',
				'required':'True',
				'placeholder':'รายละเอียดสเปค'
				}),

		}
		labels = {
			'parts_cat_name':'ชื่อชนิดวัสดุคอมพิวเตอร์',
			'parts_sub_name':'รายละเอียดสเปค',
		}

class AddStockPartsForm(forms.ModelForm):
		
	class Meta:
		model = PartsStock
		fields = "__all__"

		widgets = {

			'parts_cat_name': forms.Select(attrs={
        		'class': 'form-control',
    			}),
    		'parts_sub_name': forms.Select(attrs={
        		'class': 'form-control',
    			}),		
			'parts_details':forms.TextInput(
				attrs={'class':'form-control',
				'required':'True',
				'placeholder':'รายละเอียดสเปค'
				}),
			'price' : forms.NumberInput(
				attrs={
				'class': 'form-control',
				'required': 'True',
				'placeholder': 'ราคาต่อหน่วย'
				}),
			'amount' : forms.NumberInput(
				attrs={
				'class': 'form-control',
				'required': 'True',
				'placeholder': 'ระบุจำนวนชิ้น'
				})

		}
		labels = {
			'parts_cat_name':'ชื่อวัสดุ',
			'parts_sub_name':'สเปค',
			'parts_details':'รายละเอียดสเปค',
			'price':'ราคาต่อหน่วย',
			'amount':'รับเข้าจำนวน',
		}
 
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if 'parts_cat_name' in self.data:
			try:
				cat_id = int(self.data.get('parts_cat_name'))
				self.fields['parts_sub_name'].queryset = PartsSubCatName.objects.filter(parts_cat_name_id=cat_id).order_by('parts_sub_name')
			except (ValueError, TypeError):
				self.fields['parts_sub_name'].queryset = PartsSubCatName.objects.none()
		elif self.instance.pk:
			self.fields['parts_sub_name'].queryset = PartsSubCatName.objects.filter(parts_cat_name=self.instance.parts_cat_name).order_by('parts_sub_name')

class AddTake_A_PartsForm(forms.ModelForm):
	
	#captcha = CaptchaField()
	#img_server = MultipleFileField(label = 'เพิ่มภาพ',required=True) 

	# To query and display data in a Django form using forms.Select()
	computer_id = forms.ModelChoiceField(
		queryset=RepairAndPartChange.objects.filter(repairstatus_id=3,part_cat_change__isnull=True),  # Query the database for categorie spart_cat_change__isnull=True 
		widget=forms.Select(attrs={'class': 'form-control'}),  # Optional styling
		empty_label="เลือกเครื่องที่ส่งซ่อม",
		label = "เครื่องที่ส่งซ่อม",  # Optional placeholder
	)
	class Meta:
		model = ItemsRepairOrderParts
		fields = ['repair_id', 'computer_id', 'part_id', 'part_sn', 'part_amount_use']

		widgets = { 
			'repair_id':forms.TextInput(
				attrs={'class':'form-control',
				'readonly':'readonly',
				}),

			'part_id':forms.Select(
				attrs={'class':'form-control',
				'required':'True',
				'placeholder':'เลือกประเภทวัสดุ'
				}),
			'part_sn':forms.TextInput(
				attrs={'class':'form-control',
				'required':'True',
				'placeholder':'หมายเลข s/n'}),

			'part_amount_use' : forms.NumberInput(
				attrs={
				'class': 'form-control',
				'required': 'True',
				'placeholder': 'ระบุจำนวนชิ้น',
				
				}),
			'user_order' : forms.HiddenInput(),
			'admin_recorder' : forms.HiddenInput(),

		}
		labels = {
			'repair_id':'หมายเลขการซ่อม',
			'computer_id':'เครื่องที่ส่งซ่อม',
			'part_id':'ชนิดวัสดุ',
			'part_sn':'หมายเลข s/n',
			'part_amount_use':'จำนวนเบิก'			
			
		}

