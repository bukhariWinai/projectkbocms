from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from djmoney.models.fields import MoneyField
from colorfield.fields import ColorField
from django.utils.text import slugify  # New
from django.urls import reverse  # New
#import qrcode
from django.utils import timezone
from datetime import date
from datetime import datetime
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw

class ProfileUser(models.Model):
	titlename = (
		('นาย','นาย'),
		('นางสาว','นางสาว'),
		('นาง','นาง'),
		('ว่าที่ร้อยตรี','ว่าที่ร้อยตรี'),
		)

	grp = (
		('admin','admin'),
		('superuser','superuser'),
		('editer','editer'),
		('reporter','reporter'),
		('trainee','trainee'),
		)

	titlename = models.CharField(max_length=20,null=True,blank=True,choices=titlename)
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	user_active = models.BooleanField(default=True,blank=True,null=True)
	photo = models.ImageField(upload_to="ImageUserProfile",null=True,blank=True,default='user.jpg')
	jobposition_name = models.ForeignKey('jobposition',on_delete=models.CASCADE,null=True,blank=True)
	usergroup = models.CharField(max_length=100,null=True,blank=True,choices=grp)
	sections = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):		
		return f"{self.user.first_name} {self.user.last_name}"

class jobposition(models.Model):
	jobposition_name = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.jobposition_name

class PhotoHeaderHomePage(models.Model):
		
	date = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=200,null=True,blank=True)
	post = models.TextField(max_length=1000,null=True,blank=True)
	photoheader = models.ImageField(upload_to ='photoheader',null=True,blank=True,default='defaultpicture.jpg')

	def __str__(self):
		return self.title

###################### start kbo_news ################### 
class News(models.Model): #model @ ข่าวทั่วไป ผู้บริหาร กลุ่มงาน ฯ
	date = models.DateTimeField(blank=True,null=True )#auto_now_add=True,
	title = models.CharField(max_length=500,null=True,blank=True)
	post = RichTextField(null=True,blank=True)
	title_photo = models.ImageField(upload_to ='title_photo',null=True,blank=True,default='defaultpicture.jpg')
	reporter = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)
	section = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)
	category = models.ForeignKey('NewsCategory',on_delete=models.CASCADE,null=True,blank=True)
	slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)  #new

	def __str__(self):
		return self.post[:10]+"..."
'''
	def get_absolute_url(self):
		return reverse('newsdetails_page', kwargs={'slug': self.slug}) #new

	def save(self, *args, **kwargs):#new

		self.slug = slugify(self.post)
		
		if not self.slug:
				slug_str = f"{self.post}"
			
		self.slug = slugify(self.post)
		super(News, self).save(*args, **kwargs)
'''
class NewsPhoto(models.Model):
	news_id =  models.ForeignKey('News',on_delete=models.CASCADE,null=True,blank=True)
	news_photo = models.ImageField(upload_to='news_photo1',null=True,blank=True,default='defaultpicture.jpg')

	def __str__(self):
		return f"{self.id}"


###################### end kbo_news ################### 

class AboutUs(models.Model): #model @ บทความสุขภาพ
	date = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=200,null=True,blank=True)
	post = models.TextField(max_length=1000,null=True,blank=True)
	photo1au = models.ImageField(upload_to ='photo1au',null=True,blank=True,default='defaultpicture.jpg')	
	link_Utube = models.CharField(max_length=100,null=True,blank=True)
	reporter = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)
	#ให้มี ฟิวด์ เพื่อ แยกชนิด บทความ สุขภาพ หรือ นวัตกรรมสุขภาพต่างๆ แสดงหน้า บทความ ใน สอง คอลัมท์

	def __str__(self):
		return self.title

class ProgramOffice(models.Model):
	program_name = models.CharField(max_length=100,null=True,blank=True)
	link = models.CharField(max_length=100,null=True,blank=True)
	program_photo = models.ImageField(upload_to ='programphoto',null=True,blank=True,default='')
	font_aweasome = models.ForeignKey('FontAweasom',on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.program_name

class IconAds(models.Model): #model @ icon warp

	icon = models.ImageField(upload_to ='icon',null=True,blank=True)
	link = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.link

class LinkExternal(models.Model): #model @ icon warp

	icon = models.ImageField(upload_to ='icon',null=True,blank=True,default="")
	text = models.CharField(max_length=100,null=True,blank=True)
	linkurl = models.CharField(max_length=100,null=True,blank=True)
	facebook = models.CharField(max_length=50,null=True,blank=True)
	bg = models.ImageField(upload_to ='bg',null=True,blank=True,default="")
	
	def __str__(self):
		return self.text

class FontAweasom(models.Model): #model @ icon warp
	
	fontname = models.CharField(max_length=100,null=True,blank=True)
	font = models.ImageField(upload_to ='Fontaweasom',null=True,blank=True)
	
	def __str__(self):
		return self.fontname

class OurServices(models.Model): #model @ คลินิก สสจ.กระบี่
	date = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=200,null=True,blank=True)
	image1 = models.ImageField(upload_to ='sevicephoto',null=True,blank=True,default='defaultpicture.jpg')
	image2 = models.ImageField(upload_to ='sevicephoto',null=True,blank=True,default='defaultpicture.jpg')
	image3 = models.ImageField(upload_to ='sevicephoto',null=True,blank=True,default='defaultpicture.jpg')
	msg = models.TextField(max_length=1000,null=True,blank=True)
	section = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.msg

class Compliment(models.Model): #model @ เรื่องเด่น สสจ.กระบี่
	date = models.DateTimeField(null=True,blank=True)
	trophy = models.ImageField(upload_to ='trophy',null=True,blank=True,default='defaultpicture.jpg')
	msg = models.TextField(max_length=200,null=True,blank=True)
	nametrophy = models.CharField(max_length=100,null=True,blank=True)
	section = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)


	def __str__(self):
		return self.msg

class Doctor(models.Model): #model @ ผู้บริหาร สสจ.กระบี่
	name = models.CharField(max_length=100,null=True,blank=True)
	lastname = models.CharField(max_length=100,null=True,blank=True)
	photo_doc = models.ImageField(upload_to ='doctor',null=True,blank=True,default='defaultpicture.jpg')
	msg = models.CharField(max_length=200,null=True,blank=True)
	scholarposition = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.name

class CallToAction(models.Model):
	date = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=200,null=True,blank=True)
	post = models.TextField(max_length=1000,null=True,blank=True)
	photo1ac = models.ImageField(upload_to ='photo1ac',null=True,blank=True,default='defaultpicture.jpg')
	link_Utube = models.CharField(max_length=100,null=True,blank=True)
	
	def __str__(self):
		return self.title


class NewsCategory(models.Model):
	categ = models.CharField(max_length=50,null=True,blank=True)
	def __str__(self):
		return self.categ

class Sections(models.Model):
	sectionsname = models.CharField(max_length=50,null=True,blank=True)
	photosect = models.ImageField(upload_to ='photosections',null=True,blank=True,default='defaultpicture.jpg')
	tel = models.CharField(max_length=50,null=True,blank=True)
	def __str__(self):
		return self.sectionsname


class Comdealer(models.Model):
	dealername = models.CharField(max_length=50,null=True,blank=True)
	dealer_addr = models.TextField(max_length=500,null=True,blank=True)
	tel = models.CharField(max_length=50,null=True,blank=True)

	def __str__(self):
		return self.dealername

class ProjectBudget(models.Model):
	budgetname = models.CharField(max_length=100,null=True,blank=True)
	def __str__(self):
		return self.budgetname

class ComputerType(models.Model):
	comtypename = models.CharField(max_length=100,null=True,blank=True)
	def __str__(self):
		return self.comtypename

class ComRequest(models.Model): #ขอสนับสนุนคอมพิวเตอร์

	requesttype = (
		('ขอใหม่','ขอใหม่'),
		('ทดแทนของเดิม','ทดแทนของเดิม'),
		('เพิ่มประสิทธิภาพ','เพิ่มประสิทธิภาพ'),

		)

	user = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)
	jobdis = models.TextField(max_length=500,null=True,blank=True)
	date = models.DateTimeField(null=True,blank=True)
	request = models.TextField(max_length=100,null=True,blank=True,choices=requesttype)
	comtype = models.ForeignKey('ComputerType',on_delete=models.CASCADE,null=True,blank=True)		
	section = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)
	bookfile = models.FileField(upload_to ='bookfile',null=True,blank=True)
	consider_result = models.BooleanField(default=False,null=True,blank=True)

	def __str__(self):
		return self.user.user.first_name

class FileDownload(models.Model): #อัพโหลดเพื่อโหลดไฟล์

	postdate = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=500,null=True,blank=True)
	file = models.FileField(upload_to ='filedownload',null=True,blank=True)	
	section = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)
	category = models.ForeignKey('NewsCategory',on_delete=models.CASCADE,null=True,blank=True)
	user = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.title

class ConferenceSchedule(models.Model): #อัพโหลดเพื่อโหลดไฟล์

	postdate = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=500,null=True,blank=True)
	schedule = RichTextField(null=True,blank=True)
	file = models.FileField(upload_to ='filedownload',null=True,blank=True)	
	category = models.ForeignKey('NewsCategory',on_delete=models.CASCADE,null=True,blank=True)
	user = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.title

class ComputerAccessory(models.Model): #model @ เครื่องคอมพิวเตอร์

	hddtype = (
		('ไม่มีฮาร์ดดิสก์','ไม่มีฮาร์ดดิสก์'),
		('SSD','SSD'),
		('HDD','HDD'),
		)
	timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	date = models.DateTimeField(null=True,blank=True)
	comphoto = models.ImageField(upload_to ='comphoto',null=True,blank=True,default='defaultpicture.jpg')	
	deviceID = models.CharField(max_length=50,null=True,blank=True)
	comserailnumber = models.CharField(max_length=50,null=True,blank=True)
	comtype = models.ForeignKey('ComputerType',on_delete=models.CASCADE,null=True,blank=True)
	comborrow = models.BooleanField(default=False,null=True,blank=True)#เป็๋นเครื่องยี่มใช้งานหรือมั้ย  default = false
	combranding = models.ForeignKey('ComBranding',on_delete=models.CASCADE,null=True,blank=True)
	commodel = models.CharField(max_length=100,null=True,blank=True)
	comspec = models.TextField(max_length=500,null=True,blank=True)
	hddtype = models.TextField(max_length=500,null=True,blank=True,choices=hddtype,default='SSD')	#ckbox ssd hdd
	comprice = models.IntegerField(null=True,blank=True)		
	comdateregister = models.DateTimeField(null=True,blank=True)
	comldealer = models.ForeignKey('Comdealer',on_delete=models.CASCADE,null=True,blank=True)	
	budgetproject = models.ForeignKey('ProjectBudget',on_delete=models.CASCADE,null=True,blank=True)
	projectnumber = models.CharField(max_length=50,null=True,blank=True)		
	comstatus = models.ForeignKey('RepairStatus',on_delete=models.CASCADE,null=True,blank=True,default=4)
	comoslicense = models.BooleanField(default=True,null=True,blank=True) # มี ลิขสิทธ์หรือมั้ย
	comofficelicense = models.BooleanField(default=True,null=True,blank=True) # มี ลิขสิทธ์หรือมั้ย
	remark = models.TextField(max_length=100,null=True,blank=True)
	owner = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)
	section = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)
	dataapprove = models.BooleanField(default=False,null=True,blank=True) # มี การตรวจสอบความถูกต้องของข้อมูล
	date_approve = models.DateTimeField(auto_now_add=False,null=True,blank=True) # มี วันที่ การตรวจสอบความถูกต้องของข้อมูล
	auditer = models.CharField(max_length=20,null=True,blank=True)

	def __str__(self):
		return self.owner.user.first_name #การอ้างอิง คลาส profileuser ไปยังคลาส user
		
	@property
	def computer_used(self):
		if self.comdateregister:
			# Calculate the difference in days between now and comdateregister
			now = timezone.now()
			delta = now - self.comdateregister 

			years = delta.days/365.25  # Return the number of days
			return round(years, 1)
		return 0

class FormerUser(models.Model):
		id_com = models.ForeignKey('ComputerAccessory',on_delete=models.CASCADE,null=True,blank=True)
		former_user = models.TextField(max_length=50,null=True,blank=True)
		date_return = models.DateTimeField(null=True,blank=True)

	
		#ผู้ใช้งานที่ผ่านมา

class PhotoComputerAccessory(models.Model):
	hw_number =  models.ForeignKey('ComputerAccessory',on_delete=models.CASCADE,null=True,blank=True,related_name="hw_photos")
	hw_photo = models.ImageField(upload_to='hw_photo',null=True,blank=True,default='defaultpicture.jpg')

	def __str__(self):
		return f"{self.id} {self.hw_number }"


class ComBranding(models.Model):
	brandname = models.CharField(max_length=50,null=True,blank=True)
	def __str__(self):
		return self.brandname

class RepairBookMemory(models.Model):
	bookNO = models.CharField(max_length=10,null=True,blank=True)
	dateMemory = models.DateTimeField(null=True,blank=True)
	bookFile = models.FileField(null=True,blank=True)
	def __str__(self):
		return self.bookNO

class PartsFromRepairBookMemory(models.Model):
	bookNO = models.ForeignKey('RepairBookMemory',on_delete=models.CASCADE,null=True,blank=True)
	partName = models.CharField(max_length=100,null=True,blank=True)
	amount = models.IntegerField(default=0)
	def __str__(self):
		return self.partName

class BorrowDevice(models.Model):
	datestart = models.DateTimeField(null=True,blank=True)
	comtype = models.ForeignKey('ComputerType',on_delete=models.CASCADE,null=True,blank=True)	
	deviceID = models.CharField(max_length=50,null=True,blank=True)
	deviceBrand = models.ForeignKey('ComBranding',on_delete=models.CASCADE,null=True,blank=True)
	deviceModel = models.CharField(max_length=50,null=True,blank=True)
	remark = models.TextField(max_length=100,null=True,blank=True)
	deviceStatus = models.BooleanField(default=False,null=True,blank=True)
	datefinish = models.DateTimeField(null=True,blank=True)
	returnBack = models.BooleanField(default=False,null=True,blank=True)	
	user_borrow = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True,related_name="userborrow")
	hw_id = models.ForeignKey('ComputerAccessory',on_delete=models.CASCADE,null=True,blank=True,related_name="borrow")
	admin_allowborrow = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True,related_name="userallowborrow")
	admin_returnback = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True,related_name="userreturn")
	
	def __str__(self):
		return self.user_borrow.user


class RepairStatus(models.Model):
	status = models.CharField(max_length=50,null=True,blank=True)

	def __str__(self):
		return self.status


class RepairAndPartChange(models.Model):
	datestart = models.DateTimeField(auto_now_add=True)	
	hw_id = models.ForeignKey('ComputerAccessory',on_delete=models.CASCADE,null=True,blank=True,related_name="repairs")
	owner = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True,related_name="owner")
	deviceID = models.CharField(max_length=50,null=True,blank=True)
	repaircase = models.TextField(max_length=500 ,null=True,blank=True)
	repairmethod = RichTextField(null=True,blank=True)
	clamnumber = models.TextField(max_length=20 ,null=True,blank=True)
	partphoto = models.ImageField(upload_to ='partphoto',null=True,blank=True,default='defaultpicture.jpg')
	part_cat_change = models.ForeignKey('sparepart.Parts_Category',on_delete=models.CASCADE,null=True,blank=True,default=None,related_name="parts_name_cat")
	part_sub_change = models.ForeignKey('sparepart.PartsSubCatName',on_delete=models.CASCADE,null=True,blank=True,default=None,related_name="parts_name_sub")
	repairstatus = models.ForeignKey('RepairStatus',on_delete=models.CASCADE,null=True,blank=True,default=1)
	engineering = models.ForeignKey('Comdealer',on_delete=models.CASCADE,null=True,blank=True) #ผู้ตรวจซ่อม
	memobooknumber = models.CharField(max_length=20,null=True,blank=True)
	budget = models.IntegerField(default=0,null=True,blank=True)
	datefinish = models.DateTimeField(null=True,blank=True)
	itsupport = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True,related_name="itsupport")

	def __str__(self):
		return f"{self.deviceID} {self.repaircase}"


class ServiceArtical(models.Model):
	artical = RichTextField(null=True,blank=True)
	def __str__(self):
		return self.artical


class Cyber_Alert(models.Model): #model @ เครื่องคอมพิวเตอร์
	risklevel = (
		('ความเสี่ยงสูง','ความเสี่ยงสูง'),
		('ความเสี่ยงปานกลาง','ความเสี่ยงปานกลาง'),
		('ความเสี่ยงต่ำ','ความเสี่ยงต่ำ'),
		('ยอมรับได้','ยอมรับได้'),
		)

	risktitle = models.CharField(max_length=100,null=True,blank=True)
	date = models.DateTimeField(null=True,blank=True)
	riskphoto = models.ImageField(upload_to ='riskphoto',null=True,blank=True)
	riskimpect = RichTextField(null=True,blank=True)
	risklevel = models.CharField(max_length=100,null=True,blank=True,choices=risklevel)
	riskmanage = RichTextField(null=True,blank=True)
	def __str__(self):
		return f" {self.risktitle} {self.risklevel}" 


class ITWebBlog(models.Model): #model @ คลินิก สสจ.กระบี่
	date = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=200,null=True,blank=True)
	imagewebblog = models.ImageField(upload_to ='ITWebBlog',null=True,blank=True,default='defaultpicture.jpg')	
	msg = RichTextField(null=True,blank=True)
	icon = models.ForeignKey('FontAweasom',on_delete=models.CASCADE,null=True,blank=True)
	reporter = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		
		return f"{self.date} {self.title}"


class OnePage(models.Model): #อัพโหลดเพื่อโหลดไฟล์

	postdate = models.DateTimeField(null=True,blank=True)
	title = models.CharField(max_length=500,null=True,blank=True)
	file = models.ImageField(upload_to ='onepage',null=True,blank=True,default='defaultpicture.jpg')	
	section = models.ForeignKey('Sections',on_delete=models.CASCADE,null=True,blank=True)
	category = models.ForeignKey('NewsCategory',on_delete=models.CASCADE,null=True,blank=True)
	user = models.ForeignKey('ProfileUser',on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.title






# Create your models here. 
'''
class ProcumentPart(models.Model):
	instock = models.BooleanField(default=True)
'''