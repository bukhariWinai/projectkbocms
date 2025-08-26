#custom_tags.py on cmsapp Backend
from datetime import datetime,timedelta
from django	import template
from cmsapp.models import * #นำโมเดล model จาก cmsapp มาใช้งาน
from django.db.models import Sum
from django.db.models import Q
import datetime

register = template.Library()

@register.simple_tag #this gramma
def hello_footer_tag(): # Bring and take this tag paste all pages html in your project
	return	'ยินดีต้อนรับ สำนักงานสาธารณสุขจังหวัดกระบี่' 

@register.simple_tag #this gramma
def Last_year():	
	last_year = datetime.datetime.now()
	
	return last_year

@register.simple_tag #this gramma
def count_all_news():
	all_news = News.objects.count()
	return all_news

@register.simple_tag
def count_com_request():
	com_request = ComRequest.objects.count()
	return com_request

@register.simple_tag #this gramma
def count_all_repair():
	all_repair = RepairAndPartChange.objects.all().filter(repairstatus_id=1).count() 
	return all_repair

@register.simple_tag #this gramma
def count_all_repairing():
	all_repair = RepairAndPartChange.objects.all().filter(repairstatus_id=2).count() 
	return all_repair

@register.simple_tag #this gramma
def count_all_changepart():
	all_repair = RepairAndPartChange.objects.all().filter(repairstatus_id=3).count() 
	return all_repair

@register.simple_tag #this gramma
def count_repair_done():
	all_repair = RepairAndPartChange.objects.all().filter(repairstatus_id=4).count() 
	return all_repair

@register.simple_tag #this gramma
def show_all_fix():
	all_fix = RepairAndPartChange.objects.all().filter(repairstatus_id=1)
	return all_fix

@register.simple_tag #this gramma
def show_all_fixitem():
	all_fix = RepairAndPartChange.objects.count()
	return all_fix

@register.simple_tag #this gramma
def AllDevice():
	alldevice= ComputerAccessory.objects.all().count()
	return alldevice

@register.simple_tag #this gramma 
def allOfficer():
	#officer = ProfileUser.objects.count()
	trainee = ProfileUser.objects.filter(jobposition_name_id=57).count()
	useractive = ProfileUser.objects.filter(user_active=1).count()	
	return useractive-trainee

@register.simple_tag #this gramma
def Trainee():
	trainee = ProfileUser.objects.filter(jobposition_name_id=57).count()
	return trainee

@register.simple_tag #this gramma
def PC():
	comp1 = ComputerAccessory.objects.all().filter(comtype_id=1).exclude(comstatus_id__in=['5', '6']).count()
	comp3 = ComputerAccessory.objects.all().filter(comtype_id=3).exclude(comstatus_id__in=['5', '6']).count()
	comp4 = ComputerAccessory.objects.all().filter(comtype_id=4).exclude(comstatus_id__in=['5', '6']).count()
	return comp1+comp3+comp4

@register.simple_tag #this gramma
def NB():
	
	comp5 = ComputerAccessory.objects.all().filter(comtype_id=5).exclude(comstatus_id__in=['5', '6']).count()
	comp6 = ComputerAccessory.objects.all().filter(comtype_id=6).exclude(comstatus_id__in=['5', '6']).count()
	comp7 = ComputerAccessory.objects.all().filter(comtype_id=7).exclude(comstatus_id__in=['5', '6']).count()
	return comp5+comp6+comp7

@register.simple_tag #this gramma
def AIO():	
	comp11 = ComputerAccessory.objects.all().filter(comtype_id=11).exclude(comstatus_id__in=['5', '6']).count()
	comp12 = ComputerAccessory.objects.all().filter(comtype_id=12).exclude(comstatus_id__in=['5', '6']).count()
	return comp11+comp12

# @register.simple_tag #this gramma
# def allComputer():
# 	comp1 = ComputerAccessory.objects.all().filter(comtype_id=1).count()
# 	comp3 = ComputerAccessory.objects.all().filter(comtype_id=3).count()
# 	comp4 = ComputerAccessory.objects.all().filter(comtype_id=4).count()

# 	comp5 = ComputerAccessory.objects.all().filter(comtype_id=5).count()
# 	comp6 = ComputerAccessory.objects.all().filter(comtype_id=6).count()
# 	comp7 = ComputerAccessory.objects.all().filter(comtype_id=7).count()

# 	comp11 = ComputerAccessory.objects.all().filter(comtype_id=11).count()
# 	comp12 = ComputerAccessory.objects.all().filter(comtype_id=12).count()

# 	#comp = ComputerAccessory.objects.all().filter(comtype_id=1) filter(comtype_id=5).count()
# 	return comp1+comp3+comp4+comp5+comp6+comp7+comp11+comp12


@register.simple_tag
def allComputer():
    target_ids = [1, 3, 4, 5, 6, 7, 11, 12]
    return ComputerAccessory.objects.filter(
        comtype_id__in=target_ids
    ).exclude(comstatus_id__in=['5', '6']).count()


@register.simple_tag #this gramma
def pcoff():	
	comp1 = ComputerAccessory.objects.all().filter(comtype_id=1).exclude(comstatus_id__in=['5', '6']).count()		
	return comp1



@register.simple_tag #this gramma
def pcpro1():	
	comp3 = ComputerAccessory.objects.all().filter(comtype_id=3).exclude(comstatus_id__in=['5', '6']).count()		
	return comp3

@register.simple_tag #this gramma
def pcpro2():	
	comp4 = ComputerAccessory.objects.all().filter(comtype_id=4).exclude(comstatus_id__in=['5', '6']).count()		
	return comp4

@register.simple_tag #this gramma
def nboff():	
	comp5 = ComputerAccessory.objects.all().filter(comtype_id=5).exclude(comstatus_id__in=['5', '6']).count()		
	return comp5

@register.simple_tag #this gramma
def nbpro1():	
	comp6 = ComputerAccessory.objects.all().filter(comtype_id=6).exclude(comstatus_id__in=['5', '6']).count()		
	return comp6

@register.simple_tag #this gramma
def nbpro2():	
	comp7 = ComputerAccessory.objects.all().filter(comtype_id=7).exclude(comstatus_id__in=['5', '6']).count()		
	return comp7

@register.simple_tag #this gramma
def aio_off():	
	comp11 = ComputerAccessory.objects.all().filter(comtype_id=11).exclude(comstatus_id__in=['5', '6']).count()		
	return comp11

@register.simple_tag #this gramma
def aio_pro():	
	comp12 = ComputerAccessory.objects.all().filter(comtype_id=12).exclude(comstatus_id__in=['5', '6']).count()		
	return comp12		
	
	
@register.simple_tag #this gramma
def OsLicense():
	oslicense= ComputerAccessory.objects.all().filter(comoslicense=True ).exclude(comstatus_id__in=['5', '6']).count()
	return oslicense

@register.simple_tag #this gramma
def OfficeLicense():
	officelicense = ComputerAccessory.objects.all().filter(comofficelicense=True).exclude(comstatus_id__in=['5', '6']).count()
	return officelicense

@register.simple_tag #this gramma
def NonLicense():
	nonlicense = ComputerAccessory.objects.all().filter(comofficelicense=False).exclude(comstatus_id__in=['5', '6']).count()
	return nonlicense

@register.simple_tag #this gramma
def SSDdrive():
	ssd = ComputerAccessory.objects.all().filter(hddtype="SSD").count()
	return ssd

@register.simple_tag #this gramma
def HDDdrive():
	hdd = ComputerAccessory.objects.all().filter(hddtype="HDD").count()
	return hdd	

@register.simple_tag #this gramma
def UPS():
	ups = ComputerAccessory.objects.all().filter(comtype_id=8).count()
	return ups	

@register.simple_tag #this gramma
def Scanner():
	scanner = ComputerAccessory.objects.all().filter(comtype_id=9).count()
	return scanner	

@register.simple_tag #this gramma
def Printer():
	printer = ComputerAccessory.objects.all().filter(comtype_id=10).count()
	return printer

@register.simple_tag
def itOfficer():
	it = ProfileUser.objects.all().filter(sections_id=1).count()
	return it

@register.simple_tag
def healthPromotionsOfficer():
	it = ProfileUser.objects.all().filter(sections_id=2).count()
	return it

@register.simple_tag
def pharmaOfficer():
	it = ProfileUser.objects.all().filter(sections_id=3).count()
	return it

@register.simple_tag
def tmdOfficer():
	it = ProfileUser.objects.all().filter(sections_id=4).count()
	return it		

@register.simple_tag
def hrOfficer():
	it = ProfileUser.objects.all().filter(sections_id=5).count()
	return it

@register.simple_tag
def lawOfficer():
	it = ProfileUser.objects.all().filter(sections_id=6).count()
	return it

@register.simple_tag
def planOfficer():
	it = ProfileUser.objects.all().filter(sections_id=7).count()

@register.simple_tag
def devOfficer():
	it = ProfileUser.objects.all().filter(sections_id=8).count()
	return it

@register.simple_tag
def ncdOfficer():
	it = ProfileUser.objects.all().filter(sections_id=9).count()
	return it

@register.simple_tag
def cdOfficer():
	it = ProfileUser.objects.all().filter(sections_id=10).count()
	return it

@register.simple_tag
def envOfficer():
	it = ProfileUser.objects.all().filter(sections_id=12).count()
	return it

@register.simple_tag
def insureOfficer():
	it = ProfileUser.objects.all().filter(sections_id=13).count()
	return it

@register.simple_tag
def mngOfficer():
	it = ProfileUser.objects.all().filter(sections_id=14).count()
	return it

@register.simple_tag
def dentOfficer():
	it = ProfileUser.objects.all().filter(sections_id=16).count()
	return it


@register.simple_tag #this gramma
def AllBorrow():
	borrow1 = BorrowDevice.objects.all().filter(deviceStatus=True).count() 
	borrow2 = BorrowDevice.objects.all().filter(deviceStatus=False).count() 
	return borrow1 + borrow2

@register.simple_tag #this gramma
def AllBorrowDone():
	borrow = BorrowDevice.objects.all().filter(returnBack=True).count() 
	return borrow

@register.simple_tag #this gramma
def AllBorrowUsing():
	borrow = BorrowDevice.objects.all().filter(returnBack=False).count() 
	return borrow

@register.simple_tag
def repair_budget():
	budget = RepairAndPartChange.objects.aggregate(total=Sum('budget'))
	total = budget['total'] or 0
	return f"{total:,.2f}"  # return 0 if no records exist


#########################
#คอมรอจำหน่าย จำหน่าย
#########################
@register.simple_tag #this gramma com outdate
def com_outdate():	
	comp_outdate = ComputerAccessory.objects.all().filter(comstatus_id=5).count()		
	return comp_outdate

@register.simple_tag #this gramma com จำหน่ายแล้ว
def com_retry():	
	comp_off = ComputerAccessory.objects.all().filter(comstatus_id=6).count()		
	return comp_off

########################
# ##########################
thai_months = [
	"",
	"มกราคม",
	"กุมภาพันธ์",
	"มีนาคม",
	"เมษายน",
	"พฤษภาคม",
	"มิถุนายน",
	"กรกฎาคม",
	"สิงหาคม",
	"กันยายน",
	"ตุลาคม",
	"พฤศจิกายน",
	"ธันวาคม",
]


@register.simple_tag
def thai_date(value):
	if not isinstance(value, (datetime.date, datetime.datetime)):
		return value
	day = value.day
	month = thai_months[value.month]
	year = value.year + 543
	return f"{day} {month} {year}"


@register.simple_tag
def thai_date_short(value):
	if not isinstance(value, (datetime.date, datetime.datetime)):
		return value
	day = f"{value.day:02d}"
	month = f"{value.month:02d}"
	year = value.year + 543
	return f"{day}/{month}/{year}"



