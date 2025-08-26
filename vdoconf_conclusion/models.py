
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class VdoconfConclusion(models.Model):
	vdoconfdate= models.DateTimeField(blank=True)	
	vdoconftitle = models.CharField(max_length=50,blank=True,null=True)
	confDetail = RichTextField(blank=True,null=True)
	link_url_vdo = models.CharField(max_length=50,blank=True,null=True)
	user = models.ForeignKey('cmsapp.ProfileUser',on_delete=models.CASCADE,null=True,blank=True)

	
	def __str__(self):
		return self.vdoconftitle

class ImageConf(models.Model):
	vdoconf_id = models.ForeignKey('VdoconfConclusion',on_delete=models.CASCADE,null=True,blank=True)
	img_vdoconf = models.ImageField(upload_to='imgvdoconf',null=True,blank=True)	

	def __str__(self):
		return self.server_id

class VdoConf(models.Model):
	vdoconf_id = models.ForeignKey('VdoconfConclusion',on_delete=models.CASCADE,null=True,blank=True)
	playlist = models.ImageField(upload_to='vdoconf',null=True,blank=True)	

	def __str__(self):
		return self.vdoconf_id

