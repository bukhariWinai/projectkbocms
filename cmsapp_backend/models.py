from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
#from ckeditor_uploader.fields import RichTextUploadingField
#from .models import ProfileUser
#from cmsapp.models import RepairAndPartChange
#from cmsapp.models import ProfileUser

class Trainee(models.Model):
	title_name = models.ForeignKey('TitleName',on_delete=models.CASCADE,blank=True,null=True)
	traineeUser_id = models.ForeignKey('cmsapp.ProfileUser',on_delete=models.CASCADE,blank=True,null=True)
	Trainee_firstname = models.CharField(max_length=100)
	Trainee_lastname = models.CharField(max_length=100)
	Trainee_school = models.ForeignKey('School',on_delete=models.CASCADE,null=True,blank=True)
	Trainee_degree = models.ForeignKey('Degree',on_delete=models.CASCADE,null=True,blank=True)
	subject = models.CharField(max_length=100,blank=True,null=True)
	subject_ability = models.TextField(max_length=100,blank=True,null=True)
	Training_start = models.DateTimeField()
	Training_finish = models.DateTimeField()
	Training_phone = models.CharField(max_length=10)
	teacher_name = models.CharField(max_length=50,blank=True)
	phone_teacher = models.CharField(max_length=10,blank=True)
	photograph = models.FileField(upload_to ='TrianeePhoto',null=True,blank=True,default='user.jpg')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.Trainee_firstname

class School(models.Model):
	school_name = models.CharField(max_length=100)
	school_province = models.CharField(max_length=100)
	
	def __str__(self):
		return self.school_name

class TitleName(models.Model):
	title_name = models.CharField(max_length=100)	
	def __str__(self):
		return self.title_name


class Degree(models.Model):
	degree_name = models.CharField(max_length=100)
	description = models.TextField()    
	def __str__(self):
		return self.degree_name

class DailyWorkReport(models.Model):
	usertrinee = models.ForeignKey('cmsapp.ProfileUser',on_delete=models.CASCADE,null=True,blank=True)
	date = models.DateField(auto_now_add=True)
	workitem = models.CharField(max_length=100,blank=True,null=True)
	workdisc = RichTextField(blank=True,null=True)
	rating = models.IntegerField(blank=True,null=True)
	result = models.BooleanField(default=False)
	remark = RichTextField(blank=True,null=True)
	admin_control = models.ForeignKey('cmsapp.ProfileUser',on_delete=models.CASCADE,null=True,blank=True,related_name="admin_controls")

	def __str__(self):
		return f"{self.usertrinee} - {self.date.date()} - {self.workitem} - {self.result}"

	class Meta:
		verbose_name = "Daily Work Report"
		verbose_name_plural = "Daily Work Reports"
		ordering = ['-date']



class ImagesCloud(models.Model):
	workid = models.ForeignKey('DailyWorkReport',on_delete=models.CASCADE,null=True,blank=True)
	images = models.ImageField(upload_to ='images-cloud',null=True,blank=True,default='defaultpicture.jpg')

	def __str__(self):
		return f"image {self.workid}"