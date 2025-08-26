# import form class from django
from django import forms
from captcha.fields import CaptchaField
from cmsapp.models import *
from .models import *
from sparepart.models import *
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User


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

class Register_Form(forms.ModelForm):
	captcha = CaptchaField()
	# captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password')
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control'}),
			'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.TextInput(attrs={'class': 'form-control'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control'}),
		}
		labels = {
			'username':'ชื่อผู้ใช้',
			'first_name':'ชื่อ',
			'last_name':'นามสกุล',
			'email':'อีเมลล์',
			'password':'รหัสผ่าน',
		}

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError("ชื่อผู้ใช้นี้มีในระบบแล้ว")
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("อีเมลนี้มีในระบบแล้ว")
		return email

class NewsForm(forms.ModelForm):
	# specify the name of model to use
	#captcha = CaptchaField()
	photo1 = MultipleFileField(label = 'เพิ่มภาพประกอบข่าว (2-3ภาพ)',required=True) 
	class Meta:
		model = News
		fields = "__all__"

		widgets = { 
			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'post':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'reporter':forms.HiddenInput(),  #auto input field when login 
			'section':forms.Select(attrs={'class':'form-control','required':'True',}),
			'category':forms.Select(attrs={'class':'form-control','required':'True',}),
			'slug':forms.TextInput(attrs={'class':'form-control',}),

		}
		labels = {
			'date':'วันที่',
			'title':'หัวข้อข่าว',
			'post':'เนื้อหาข่าว',			
							#'reporter':'ผู้เขียน', เพื่มอัตโนมัติ 'reporter':forms.HiddenInput(),
			'section':'กลุ่มงาน',
			'category':'หมวดข่าว',
			'slug':'ลิงค์ข่าว',	
			'title_photo':'เพิ่มพาดหัวข่าว 1 ภาพ',		
		}


class AddArtical_Form(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = AboutUs
		fields = "__all__"

		widgets = {

			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'post':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			#'photo1au':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			#'photo2au':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'link_Utube':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			 #'reporter':forms.Select(attrs={'class':'form-control','required':'True',}),
			'reporter': forms.HiddenInput(),

		}

		labels = {

			'date':'วันที่',
			'title':'หัวข้อข่าว',
			'post':'เนื้อหาข่าว',
			'photo1au':'ภาพประกอบ',			
			'link_Utube':'ลิงค์วิดีโอจาก:YOUTUBE',			
			'reporter':'ผู้เขียน',

		}

class AddConferenceForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = ConferenceSchedule
		fields = "__all__"

		widgets = {

			'postdate':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'schedule':forms.TextInput(attrs={'class':'form-control','required':'True',}),
						
			#'file':forms.FileField(), #have no this attrs in widget django and must use defualt.
			'category':forms.Select(attrs={'class':'form-control','required':'True',}),
			#'user':forms.Select(attrs={'class':'form-control','required':'True',}),
			'user': forms.HiddenInput(),

		}

		labels = {

			'postdate':'วันที่',
			'title':'หัวข้อประชุม',
			'schedule':'วาระการประชุม',
			'file':'ไฟล์แนบวาระการประชุม',			
			'category':'กลุ่มการประชุม',			
			'user':'ผู้เขียน',

		}

class AddOurServiceForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = OurServices
		fields = "__all__"

		widgets = {

			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'msg':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			
			
			#'file':forms.FileField(), #have no this attrs in widget django and must use defualt.
			'section':forms.Select(attrs={'class':'form-control','required':'True',}),
			
		}

		labels = {

			'date':'วันที่',
			'title':'ชื่อบริการหน่วยงาน',
			'image1':'ภาพประกอบ1',
			'image2':'ภาพประกอบ2',
			'image3':'ภาพประกอบ3',

			'msg':'รายละเอียดงานบริการ',			
			'section':'กลุ่มงาน',		

		}

class AddFileDownloadForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = FileDownload
		fields = "__all__"

		widgets = {

			'postdate':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),									
			#'file':forms.FileField(), #have no this attrs in widget django and must use defualt.
			'section':forms.Select(attrs={'class':'form-control','required':'True',}),
			'category':forms.Select(attrs={'class':'form-control','required':'True',}),
			#'user':forms.Select(attrs={'class':'form-control','required':'True',}),
			'user':forms.HiddenInput(),

		}

		labels = {

			'postdate':'วันที่',
			'title':'หัวข้อประกาศ',			
			'file':'ไฟล์แนบ',	
			'section':'จากกลุ่มงาน',		
			'category':'หมวดหมู่ประกาศ',			
			'user':'ผู้ประกาศ',

		}

class AddPhotoHeadHomePageForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = PhotoHeaderHomePage
		fields = "__all__"

		widgets = {

			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),	
			'post':forms.TextInput(attrs={'class':'form-control','required':'True',}),									
			#'file':forms.FileField(), #have no this attrs in widget django and must use defualt

		}

		labels = {

			'date':'วันที่',
			'title':'หัวข้อประกาศ',			
			'post':'เนื้อหา',	
			'photoheader':'ภาพแบนเนอร์',		
						
		}

class AddDocterForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = Doctor
		fields = "__all__"

		widgets = {

			'name':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'lastname':forms.TextInput(attrs={'class':'form-control','required':'True',}),	
			'msg':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'scholarposition':forms.TextInput(attrs={'class':'form-control','required':'True',}),									

			#'file':forms.FileField(), #have no this attrs in widget django and must use defualt

		}

		labels = {

			'name':'ชื่อ',
			'lastname':'นามสกุล',			
			'msg':'ข้อความ',	
			'scholarposition':'ตำแหน่ง',		
			'photo_doc':'รูปผู้บริหาร',							
		}

class AddFontAweasomeForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = FontAweasom
		fields = "__all__"

		widgets = {

			'fontname':forms.TextInput(attrs={'class':'form-control','required':'True',}),
												
		}

		labels = {

			'fontname':'ชื่อฟอนท์',
			'font':'รูปฟอนท์',						
						
		}

class AddFormerUserForm(forms.ModelForm):
	
	class Meta:
		model = FormerUser
		fields = "__all__"

		widgets = {
			'id_com':forms.HiddenInput(),
			'former_user':forms.TextInput(attrs={'class':'form-control','placeholder': 'เพิ่มผู้ใช้งานก่อนหน้า','required':'True',}),
			'date_return':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
											
		}
		labels = {

			'former_user':'เพิ่มผู้ใช้งาน',
			'date_return':'วันที่ส่งมอบคืน',						
		}

class AddNewCategoryForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = NewsCategory
		fields = "__all__"

		widgets = {

			'categ':forms.TextInput(attrs={'class':'form-control','placeholder': 'เพิ่มชื่อหมวดหมู่บทความ','required':'True',}),												

		}

		labels = {

			'categ':'ชื่อหมวดหมู่ข่าว',
						
		}

class AddSectionForm(forms.ModelForm):
	# scaptcha = CaptchaField()
	class Meta:
		model = Sections
		fields = "__all__"

		widgets = {

			'sectionsname':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'tel':forms.TextInput(attrs={'class':'form-control','required':'True',}),

		}

		labels = {

			'sectionsname':'ชื่อกลุ่มงานหน่วยงาน',
			'photosect':'รูปกลุ่มงาน',
			'tel':'เบอร์ติดต่อหน่วยงาน',						
		}

class AddIconAdsForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = IconAds
		fields = "__all__"

		widgets = {

			'link':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			
			#'file':forms.FileField(), #have no this attrs in widget django and must use defualt

		}

		labels = {

			'icon':'รูปแบนเนอร์',
			'link':'ลิ้งค์ URL',							
		}

class AddLinkExternalForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = LinkExternal
		fields = "__all__"

		widgets = {

			'text':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'linkurl':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'facebook':forms.TextInput(attrs={'class':'form-control','required':'True',}),
						
		}

		labels = {

			'icon':'รูป icon หน่วยงาน',
			'text':'ชื่อหน่วยงาน',
			'linkurl':'URL เว็บหน่วยงาน',
			'facebook':'URL facebook',
			'bg':'ภาพพื้นหลัง',
							
		}

class AddOnePageForm(forms.ModelForm):
	# captcha = CaptchaField()
	class Meta:
		model = OnePage
		fields = "__all__"

		widgets = {

			'postdate':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),	
			'section':forms.Select(attrs={'class':'form-control','required':'True',}),
			'category':forms.Select(attrs={'class':'form-control','required':'True',}),
			#'user':forms.Select(attrs={'class':'form-control','required':'True',}),
			'user':forms.HiddenInput(),

			#'file':forms.FileField(), #have no this attrs in widget django and must use defualt

		}

		labels = {

			'postdate':'วันที่',
			'title':'ชื่อเรื่อง',
			'file':'ไฟล์แนบ OnePage',
			'section':'กลุ่มงาน',
			'category':'หมวดหมู่',
			'user':'ผู้รายงาน',						

		}

class AddComReqForm(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = ComRequest
		fields = "__all__"

		widgets = {

			'user':forms.HiddenInput(),
			'jobdis':forms.TextInput(attrs={'class':'form-control','required':'True',}),	
			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'request':forms.Select(attrs={'class':'form-control','required':'True',}),
			'comtype':forms.Select(attrs={'class':'form-control','required':'True',}),
			#'comspec':forms.Select(attrs={'class':'form-control','required':'True',}),
			'section':forms.Select(attrs={'class':'form-control','required':'True',}),
			'consider_result':forms.HiddenInput()

		}

		labels = {

			'user':'ชื่อผู้ขอ',
			'jobdis':'รายละเอียดงานรับผิดชอบ',
			'date':'วันที่ขอ',
			'request':'ลักษณะการขอ',
			'comtype':'ประเภทเครื่อง',
			#'comspec':'สเปคเครื่อง',
			'section':'กลุ่มงาน',
			'section':'กลุ่มงาน',
			'bookfile':'ไฟล์แนบบันทึกขัอความ',
		}

class AddComAccessoryForm(forms.ModelForm):
	# Upload multiple files
	comphoto = MultipleFileField(label = 'อัพโหลดภาพ', required=True)

	# Boolean fields
	# comborrow = forms.BooleanField(label='อุปกรณ์ยืมใช้งาน', required=False)
	comborrow = forms.BooleanField(label='อุปกรณ์ยืมใช้งาน', required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
	comoslicense = forms.BooleanField(label='ลิขสิทธิ์ระบบปฏิบัติการ', required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
	comofficelicense = forms.BooleanField(label='ลิขสิทธิ์โปรแกรมสำนักงาน', required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
	dataapprove = forms.BooleanField(label='ความถูกต้องข้อมูล', required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

	class Meta:
		model = ComputerAccessory
		fields = "__all__"

		widgets = {
			'date': forms.DateTimeInput(attrs={
				'type': 'datetime-local',
				'class': 'form-control',
				'required': True
			}),
			'deviceID': forms.TextInput(attrs={
				'class': 'form-control',
				'required': True
			}),

			'comserailnumber': forms.TextInput(attrs={
				'class': 'form-control',
				'required': True
			}),
			'comtype': forms.Select(attrs={'class': 'form-control', 'required': True}),
			'combranding': forms.Select(attrs={'class': 'form-control', 'required': True}),
			'commodel': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
			'comspec': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
			'hddtype': forms.Select(attrs={'class': 'form-control', 'required': True}),
			'comprice': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
			'comdateregister': forms.DateTimeInput(attrs={
				'type': 'datetime-local',
				'class': 'form-control',
				'required': True
			}),
			'comldealer': forms.Select(attrs={'class': 'form-control', 'required': True}),
			'budgetproject': forms.Select(attrs={'class': 'form-control', 'required': True}),
			'projectnumber': forms.TextInput(attrs={'class': 'form-control'}),
			'comstatus': forms.Select(attrs={'class': 'form-control', 'required': True}),
			'remark': forms.TextInput(attrs={'class': 'form-control'}),
			'owner': forms.Select(attrs={'class': 'form-control select2', 'required': True}),
			'section': forms.Select(attrs={'class': 'form-control', 'required': True}),
			'date_approve': forms.DateTimeInput(attrs={
				'type': 'datetime-local',
				'class': 'form-control',
				'required': True
			}),
			'auditer': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
		}

		labels = {
			'date': 'วันที่ลงบันทึก',
			'deviceID': 'เลขครุภัณฑ์',
			'comserailnumber': 'เลขซีเรียล (SN)',
			'comtype': 'ประเภท',
			'combranding': 'ยี่ห้อ',
			'commodel': 'รุ่น',
			'comspec': 'คุณลักษณะ',
			'hddtype': 'ชนิดฮาร์ดไดรฟ์',
			'comprice': 'ราคาขาย',
			'comdateregister': 'วันรับ',
			'comldealer': 'บริษัท',
			'budgetproject': 'โครงการ',
			'projectnumber': 'รหัสโครงการ',
			'comstatus': 'สถานะ',
			'remark': 'หมายเหตุ',
			'owner': 'ผู้รับผิดชอบ',
			'section': 'กลุ่มงาน',
			'date_approve': 'วันที่ตรวจสอบ',
			'auditer': 'ผู้ตรวจสอบ',
		}

class FormComputerUpdateDetails(forms.ModelForm):
	
	class Meta:
		model = ComputerAccessory
		fields = "__all__"	

		widgets = {
							
			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True', }),
			'deviceID':forms.TextInput(attrs={'class':'form-control','required':'True', }),
			'comserailnumber':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'comtype':forms.Select(attrs={'class':'form-control','required':'True',}),
			'combranding':forms.Select(attrs={'class':'form-control','required':'True',}),
			'commodel':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'comspec':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'hddtype':forms.Select(attrs={'class':'form-control','required':'True',}),
			'comprice':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'comdateregister':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),		
			'comldealer':forms.Select(attrs={'class':'form-control','required':'True',}),			
			'budgetproject':forms.Select(attrs={'class':'form-control','required':'True',}),
			'projectnumber':forms.TextInput(attrs={'class':'form-control'}),			
			'comstatus':forms.Select(attrs={'class':'form-control','required':'True',}),
			#'owner':forms.HiddenInput(),
			'remark' :forms.TextInput(attrs={'class':'form-control'}),
			'owner':forms.Select(attrs={'class':'form-control','required':'True',}),
			'section':forms.Select(attrs={'class':'form-control','required':'True',}),
			'date_approve':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),		
			'auditer':forms.TextInput(attrs={'class':'form-control' ,'required':'True',}),		
					
		}

		labels = {

			'date':'วันที่ลงบันทึก',						
			'deviceID':'เลขครุภัณฑ์',
			'comserailnumber':'เลขซีเรียล(sn)',
			'comtype':'ประเภท',		
			'combranding':'ยี่ห้อ',
			'commodel':'รุ่น',
			'comspec':'คุณลักษณะ',
			'hddtype':'ชนิดฮาร์ดไตร์ฟ',
			'comprice':'ราคาขาย',
			'comdateregister':'วันรับ',
			'comldealer':'บริษัท',
			'budgetproject':'โครงการ',
			'projectnumber':'รหัสโครงการ',
			'comstatus':'สถานะ',
			'comoslicense':'ลิขสิทธิ์ระบบปฏิบัติการ',
			'comofficelicense':'ลิขสิทธิ์โปรแกรมสำนักงาน',
			'remark':'หมายเหตุ',
			'owner':'ผู้รับผิดชอบ',
			'section':'กลุ่มงาน',
			'dataapprove':'ยื่นยันข้อมูล',
			'date_approve':'วันที่ตรวจสอบ',
			'auditer':'ผู้ตรวจสอบ',

		}

class UpdateUserProfileForm(forms.ModelForm):
	photo = forms.FileField(label='เลือกไฟล์รูปโปรไฟล์')
	#user_active = forms.BooleanField(label='เปิดการใช้งานสมาชิก')
	class Meta:
		model = ProfileUser
		fields = ["photo","jobposition_name","sections"]
		widgets = {

			'jobposition_name':forms.Select(attrs={'class':'form-control','required':'True',}),
			'sections':forms.Select(attrs={'class':'form-control','required':'True',}),

		}
		labels = {

			'jobposition_name':'เลือกตำแหน่ง',
			'sections':'เลือกกลุ่มงาน',

		}

class UpdateProfileUserAdminForm(forms.ModelForm):
	photo = forms.FileField(label='เลือกไฟล์รูปโปรไฟล์')
	user_active = forms.BooleanField(label='เปิดการใช้งาน',help_text="Uncheck เพื่อปิดการใช้งาน",required=False)
	class Meta:
		model = ProfileUser
		fields = ["user_active","photo","jobposition_name","usergroup","sections"]
		widgets = {

			'jobposition_name':forms.Select(attrs={'class':'form-control','required':'True',}),
			'sections':forms.Select(attrs={'class':'form-control','required':'True',}),
			'usergroup':forms.Select(attrs={'class':'form-control','required':'True',}),

		}
		labels = {

			'jobposition_name':'เลือกตำแหน่ง',
			'sections':'เลือกกลุ่มงาน',
			'usergroup':'สิทธิใช้งาน',
		}
		
class AddCyberAlertForm(forms.ModelForm):
	#captcha = CaptchaField()
	class Meta:
		model = Cyber_Alert
		fields = "__all__"

		widgets = {

			'risktitle':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'riskimpect':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'risklevel':forms.Select(attrs={'class':'form-control','required':'True',}),
			'riskmanage':forms.TextInput(attrs={'class':'form-control','required':'True',}),

		}

		labels = {

			'risktitle':'เหตุการณ์ความเสี่ยง',
			'date':'วันที่แจ้งเหตุ',
			'riskphoto':'ภาพเหตุการณ์',
			'riskimpect':'ผลกระทบ',
			'risklevel':'ระดับความเสี่ยง',
			'riskmanage':'การบริหารเหตุการณ์',						
		}

class AddCyberPolicyForm(forms.ModelForm):
	#captcha = CaptchaField()
	class Meta:
		model = ITWebBlog
		fields = "__all__"

		widgets = {
			
			'date':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),
			'title':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'msg':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'icon':forms.Select(attrs={'class':'form-control','required':'True',}),
			'reporter':forms.HiddenInput(),
			
		}

		labels = {
			
			'date':'วันที่ประกาศ',
			'title':'ชื่อประกาศ',
			'imagewebblog':'ภาพประกอบ',
			'msg':'ข้อความ',
			'icon':'icon',
			'reporter':'ผู้รายงาน',						
		}

class AddComStatusToComputerAcc(forms.ModelForm):
	class Meta:
		model = ComputerAccessory
		fields = ('comstatus',)
		widgets={'comstatus':forms.HiddenInput()}

class UpdateComStatus(forms.ModelForm):
	class Meta:
		model = ComputerAccessory
		fields = ('comstatus',)
		widgets={'comstatus':forms.HiddenInput()}

class AddRepairForm(forms.ModelForm):
	#captcha = CaptchaField()
	class Meta:
		model = RepairAndPartChange
		fields = ('repaircase','deviceID','repairstatus','owner','hw_id')

		widgets = {
			
			'repaircase' :forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'deviceID' :forms.HiddenInput(),	
			'repairstatus' :forms.HiddenInput(),			
			'owner' :forms.HiddenInput(),			
			'hw_id' :forms.HiddenInput(),			

		}

		labels = {

			'repaircase' :'อาการเสีย',			

		}

class AddRepairItemForm(forms.ModelForm):# 

	#captcha = CaptchaField()

	class Meta:
		model = RepairAndPartChange
		fields = ('repairmethod','repairstatus','engineering','itsupport')

		widgets = {
			
			'repairmethod' :CKEditorWidget(),
			'repairstatus' :forms.Select(attrs={'class':'form-control','required':'True',}),			
			'engineering' :forms.Select(attrs={'class':'form-control','required':'True',}),			
			'itsupport' : forms.HiddenInput(),			
			
		}

		labels = {

			'repairmethod' :'วีธีซ่อม',			
			'repairstatus' :'สถานะการซ่อม',			
			'engineering' :'ผู้ตรวจซ่อม',		
							
		}
	
# from django import forms
# from .models import RepairAndPartChange, Parts_Category, PartsSubCatName

class UpdateRepairItemForm(forms.ModelForm):
	part_cat_change = forms.ModelChoiceField(
		queryset=Parts_Category.objects.all(),
		required=False,
		empty_label="--- เลือกประเภทอะไหล่ ---",
		label="อะไหล่ที่เบิก",
		widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_part_cat_change'})
		# widget=forms.Select(attrs={'class': 'form-control'})
	)
	part_sub_change = forms.ModelChoiceField(
		queryset=PartsSubCatName.objects.none(),
		required=False,
		empty_label="--- เลือกสเปค ---",
		label="สเปคคุณลักษณะ",
		widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_part_sub_change'})
		
	)

	# widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_part_cat_change'})
	# widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_part_sub_change'})


	class Meta:
		model = RepairAndPartChange
		fields = (
			'clamnumber', 'repairmethod', 'part_cat_change', 'part_sub_change',
			'partphoto', 'repairstatus', 'memobooknumber', 'budget', 'datefinish'
		)

		widgets = {
			'clamnumber': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'เลขที่ใบเบิกอะไหล่/RID'
			}),
			'repairmethod': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'วิธีการซ่อม แก้ไขปัญหา'
			}),
			'partphoto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
			'repairstatus': forms.Select(attrs={'class': 'form-control'}),
			'memobooknumber': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'เลขที่บันทึกข้อความ'
			}),
			'budget': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'งบประมาณซ่อม'
			}),
			'datefinish': forms.DateTimeInput(attrs={
				'type': 'datetime-local',

				'class': 'form-control',
				'placeholder': 'วันที่ซ่อมเสร็จ'
			},
				format='%Y-%m-%dT%H:%M' ),
		}

		labels = {
			'clamnumber': 'เลขที่ใบเบิกอะไหล่',
			'repairmethod': 'วิธีการซ่อม/แก้ไขปัญหา',
			'partphoto': 'รูปอะไหล่',
			'repairstatus': 'สถานะหลังซ่อม',
			'memobooknumber': 'เลขที่บันทึกข้อความ',
			'budget': 'งบประมาณซ่อม',
			'datefinish': 'วันที่ซ่อมเสร็จ',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# ตรวจสอบว่ามีการเลือก category จาก request.POST หรือไม่
		if 'part_cat_change' in self.data:
			try:
				cat_id = int(self.data.get('part_cat_change'))
				self.fields['part_sub_change'].queryset = PartsSubCatName.objects.filter(
					parts_cat_name_id=cat_id
				)
			except (ValueError, TypeError):
				pass
		elif self.instance and self.instance.part_cat_change:
		# เวลา edit → preload subcategory ให้ตรงกับ category ที่เคยเลือกไว้
			self.fields['part_sub_change'].queryset = PartsSubCatName.objects.filter(
				parts_cat_name=self.instance.part_cat_change
			)

	# แปลง datefinish ให้ตรงกับ datetime-local
		if self.instance and self.instance.datefinish:
			from django.utils.timezone import localtime
			self.initial['datefinish'] = localtime(self.instance.datefinish).strftime('%Y-%m-%dT%H:%M')


class EditBorrowDeviceItemForm(forms.ModelForm): 
	#captcha = CaptchaField()
	class Meta:
		model = BorrowDevice
		fields = ('deviceID','deviceBrand','deviceModel','deviceStatus')
		

		widgets = {
			
			'deviceID' :forms.TextInput(attrs={'class':'form-control','required':'True',}),		
			'deviceBrand':forms.Select(attrs={'class':'form-control','required':'True',}),
			'deviceModel':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'deviceStatus' :forms.CheckboxInput(),
			
		}

		labels = {

			'deviceID': 'เลขครุภัณฑ์',			
			'deviceBrand': 'ยี่ห้อ',			
			'deviceModel' : 'รุ่น',
			'deviceStatus': 'อนุมัติการยืม',
			
		}

class EditBorrowReturnForm(forms.ModelForm): 
	#captcha = CaptchaField()
	class Meta:
		model = BorrowDevice
		fields = ('datefinish','returnBack',)
		
		widgets = {
			
			
			'datefinish':forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),		
			'returnBack': forms.CheckboxInput(attrs={
				'class': 'form-check-input',}),
			# 'itemRecorder':forms.TextInput(attrs={'class':'form-control','required':'True',}),

		}

		labels = {

			'datefinish': 'วันที่คืน',			
			'returnBack': 'คืนครุภัณฑ์',			
			# 'itemRecorder' : 'ผู้บันทึก',			
			
		}

class AddBorrowForm(forms.ModelForm):

	class Meta:
		model = BorrowDevice
		fields = ('datestart', 'comtype', 'remark', 'datefinish')
		
		widgets = {
			'datestart': forms.TextInput(attrs={
				'type': 'datetime-local',
				'class': 'form-control',
				'required': 'True',
				'placeholder': 'เลือกวันที่ขอยืม',
				'aria-label': 'วันที่ขอยืม',
				'style': 'display: inline-block;',
			}),
			'comtype': forms.Select(attrs={
				'class': 'form-control',
				'required': 'True',
				'aria-label': 'เลือกชื่ออุปกรณ์',
			}),
			'remark': forms.TextInput(attrs={
				'class': 'form-control',
				'required': 'True',
				'placeholder': 'กรอกวัตถุประสงค์การใช้งาน',
				'aria-label': 'วัตถุประสงค์การใช้งาน',
				'style': 'display: inline-block;',
			}),
			'datefinish': forms.TextInput(attrs={
				'type': 'datetime-local',
				'class': 'form-control',
				'required': 'True',
				'placeholder': 'เลือกวันที่จะคืน',
				'aria-label': 'วันที่จะคืน',
				'style': 'display: inline-block;',
			}),
		}

		labels = {
			'datestart': 'วันที่ขอยืม',
			'comtype': 'ชื่ออุปกรณ์',
			'remark': 'วัตถุประสงค์การใช้งาน',
			'datefinish': 'วันที่จะคืน',
		}

class AddTraineeForm(forms.ModelForm):
	
	class Meta:
		model = Trainee
		fields = "__all__"
		
		widgets = {
			'title_name' :forms.Select(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),			
			'Trainee_firstname':forms.TextInput(attrs={'class':'form-control','required':'True',}),
			'traineeUser_id':forms.HiddenInput(),
			'Trainee_lastname':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'Trainee_school' :forms.Select(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),
			'Trainee_degree' :forms.Select(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),
			'subject' :forms.TextInput(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),			
			'subject_ability' :forms.TextInput(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),			
			'Training_start' :forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),			
			'Training_finish' :forms.TextInput(attrs={'type':'datetime-local','class':'form-control' ,'required':'True',}),			
			'Training_phone' :forms.TextInput(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),			
			'teacher_name' :forms.TextInput(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),			
			'phone_teacher' :forms.TextInput(attrs={'type':'form-control','class':'form-control' ,'required':'True',}),			
			#'photograph' :forms.ClearableFileInput(attrs={'multiple':'True',}),			
			
		}

		labels = {
					'title_name': 'คำนำหน้าชื่อ',
					'Trainee_firstname': 'ชื่อ',				
					'Trainee_lastname': 'นามสกุล',				
					'Trainee_school': 'สถาบัน',				
					'Trainee_degree': 'ระดับชั้น',				
					'subject': 'สาขาวิชา',				
					'subject_ability': 'ทักษะพิเศษ',				
					'Training_start': 'วันที่เริ่มฝึกงาน',				
					'Training_finish': 'วันที่ฝึกเสร็จ',				
					'Training_phone': 'เบอร์ติดต่อ',				
					'teacher_name': 'อาจารย์ที่ปรึกษา',				
					'phone_teacher': 'เบอร์ติดต่ออาจารย์',				
					'photograph': 'รูปถ่ายนักศึกษา',				
			
		}

class AddProgramOfficeForm(forms.ModelForm):

	#captcha = CaptchaField()

	class Meta:
		model = ProgramOffice
		fields = "__all__"
		
		widgets = {
			
			'program_name' :forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'link':forms.TextInput(attrs={'class':'form-control','required':'True',}),
					
			'font_aweasome' :forms.Select(attrs={'class':'form-control','required':'True',}),

		}

		labels = {

			'program_name': 'ชื่อโปรแกรม',			
			'link': 'ลิงค์ WEB URL',			
			'program_photo' : 'รูปพิ้นหลังโปรแกรม',
			'font_aweasome': 'รูป shotcut',
			
		}

class AddWorkReportForm(forms.ModelForm):
	images = MultipleFileField(
		label = "อัพโหลดภาพ",
		required=True)
		
	class Meta:
		model = DailyWorkReport
		# fields = "__all__"
		fields = ('workitem','workdisc',)

		widgets = { 
			'usertrinee':forms.HiddenInput(),  #auto input field when login 
			'workitem':forms.TextInput(attrs={'class':'form-control','required':'True',}),			
			'workdisc': CKEditorWidget(),
			
		}
		labels = {
			'workitem':'หัวข้อการปฏิบัติงาน',
			'workdisc':'รายละเอียดการปฏิบัติงาน',
			
		}

class WorkRatingForm(forms.ModelForm):
	result = forms.ChoiceField(
	choices=[(True, 'ผ่าน'), (False, 'ไม่ผ่าน')],
	widget=forms.Select(attrs={'class': 'form-select'}),
	required=False,
	label='ผลการประเมิน'
)
	class Meta:
		model = DailyWorkReport
		
		fields = ('rating','result','remark','admin_control')

		widgets = { 
			
			'rating':forms.NumberInput(attrs=
				{'class':'form-control',
					'required':'True',
					'placeholder':'คะแนนผลงาน',
					'max': 5,
					'min': 1,
				}),			
			'remark':CKEditorWidget(),	
			'admin_control':forms.HiddenInput(),  #auto input field when login 			
		}
		labels = {
			
			'rating':'คะแนนผลงาน',
			'result':'ผลการประเมิน',						
			'remark':'หมายเหตุ',
			'admin_control':forms.HiddenInput(),
		}

		def clean_rating(self):
			rating = self.cleaned_data.get('rating')
			if rating > 5:
				raise forms.ValidationError('คะแนนผลงานอยู่ในช่วง 1 - 5 ')
			return rating
