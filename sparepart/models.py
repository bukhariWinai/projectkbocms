from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid

class ItemsRepairOrderParts(models.Model):
	
	created_at = models.DateTimeField(auto_now_add=True)
	repair_id = models.CharField(max_length=20,null=True,blank=True,unique=True)
	computer_id = models.ForeignKey('cmsapp.RepairAndPartChange',on_delete=models.CASCADE,blank=True,null=True,related_name="computer_id")#เลือกไปยัง computerAndAccessory.model  
	part_id = models.ForeignKey('PartsStock',on_delete=models.CASCADE,blank=True,null=True) #เลือกไปย้ง PartsName.model
	part_sn = models.CharField(max_length=30,null=True,blank=True)
	part_amount_use = models.IntegerField()
	user_order = models.ForeignKey('cmsapp.ProfileUser',on_delete=models.CASCADE,blank=True,null=True,related_name="user_oder")
	admin_recorder = models.ForeignKey('cmsapp.ProfileUser',on_delete=models.CASCADE,blank=True,null=True,related_name="admin_recorder")
	
	def save(self, *args, **kwargs):
		if not self.repair_id:
			self.repair_id = self.generate_repair_id()
		super().save(*args, **kwargs)
		
	def generate_repair_id(self):
		# ตัวอย่าง: ใช้รหัสแบบ RID-20240406001
		from datetime import datetime
		date_part = datetime.now().strftime('%Y%m%d')
		last = ItemsRepairOrderParts.objects.filter(repair_id__startswith=f"R{date_part}").count() + 1
		return f"R{date_part}{str(last).zfill(3)}"

	def __str__(self):
		return f"{self.part_id} - SN: {self.part_sn or 'N/A'}"

		

class PartRepairImage(models.Model):
	itemrepair_id = models.ForeignKey('ItemsRepairOrderParts',on_delete=models.CASCADE,null=True,blank=True)
	repair_image = models.FileField(upload_to='part_repair',null=True,blank=True,default='default.jpg')

	@property
	def pricestock(self):
		ps =  self.amount*self.price
		return ps


class PartImage(models.Model):
	partstock_id = models.ForeignKey('PartsStock',on_delete=models.CASCADE,null=True,blank=True)
	parts_image = models.FileField(upload_to='parts_image',null=True,blank=True,default='default.jpg')

class PartsSubCatName(models.Model):
	parts_cat_name = models.ForeignKey('Parts_Category',on_delete=models.CASCADE,null=True,blank=True)
	parts_sub_name = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.parts_sub_name or "-"

class Parts_Category(models.Model):
	parts_cat_name = models.CharField(max_length=100)
	def __str__(self):
		# return str(self.parts_cat_name)
		return self.parts_cat_name


class PartsStock(models.Model):
	parts_cat_name = models.ForeignKey('Parts_Category',on_delete=models.CASCADE,null=True,blank=True)
	parts_sub_name = models.ForeignKey('PartsSubCatName',on_delete=models.CASCADE,null=True,blank=True)
	parts_details = models.CharField(max_length=200,null=True,blank=True)
	price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	amount = models.IntegerField(null=True,blank=True)
	def __str__(self):
		return f"{self.parts_cat_name} > {self.parts_sub_name} - {self.parts_details or ''}"


