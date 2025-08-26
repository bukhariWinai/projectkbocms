
from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

# Create your models here.


class SerVerMainten(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	server_name = models.ForeignKey('Server',on_delete=models.CASCADE,null=True,blank=True)
	case_diag = models.CharField(max_length=100)
	resolve_Methode = RichTextField(null=True,blank=True)
	user = models.ForeignKey('cmsapp.ProfileUser',on_delete=models.CASCADE,null=True,blank=True)
	def __str__(self):
		return self.case_diag

class ImageServerRepair(models.Model):
	case_id = models.ForeignKey('SerVerMainten',on_delete=models.CASCADE,null=True,blank=True)
	img_case = models.ImageField(upload_to='imgserverdiag',null=True,blank=True)	

	def __str__(self):
		return self.case_id

class Server(models.Model):
	server_procument_id = models.CharField(max_length=50,blank=True,null=True)
	server_service_name = models.CharField(max_length=50,blank=True,null=True)
	server_brand_name = models.CharField(max_length=50,blank=True,null=True)
	server_model_name = models.CharField(max_length=50,blank=True,null=True)
	server_year_register = models.DateTimeField(blank=True,null=True)
	server_domain_name = models.CharField(max_length=50,blank=True,null=True)
	server_ip = models.CharField(max_length=50,blank=True,null=True)
	server_user = models.CharField(max_length=50,blank=True,null=True)
	server_password = models.CharField(max_length=50,blank=True,null=True)

	def __str__(self):
		return self.server_service_name

class ImageServer(models.Model):
	server_id = models.ForeignKey('Server',on_delete=models.CASCADE,null=True,blank=True)
	img_server = models.ImageField(upload_to='imgserver',null=True,blank=True)	

	def __str__(self):
		return self.server_id