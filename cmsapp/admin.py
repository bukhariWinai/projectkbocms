from django.contrib import admin
from .models import *
from cmsapp.models import *
PhotoComputerAccessory

admin.site.site_header = "สำนักงานสาธารณสุขจังหวัดกระบี่"
admin.site.site_title = "สำนักงานสาธารณสุขจังหวัดกระบี่"


class NewsManage(admin.ModelAdmin):
	list_display = ["date","title","post"]
	list_editable = ["title","post"]
	list_per_page = 2
	search_fields = ["title"]
	list_filter = ["section","reporter","category"]
	prepopulated_fields = {'slug': ('post',)} #new
admin.site.register(News,NewsManage)
admin.site.register(NewsPhoto)

class AboutUsManage(admin.ModelAdmin):
	list_display = ["date","title","photo1au","link_Utube","reporter"]
	list_editable = ["title","photo1au","link_Utube","reporter"]
	list_per_page = 4
	
admin.site.register(AboutUs,AboutUsManage)


class OurServicesManage(admin.ModelAdmin):
	list_display = ["date","title","image1","image2","image3","msg"]
	list_editable = ["title","image1","image2","image3","msg"]
	list_per_page = 4
	
admin.site.register(OurServices,OurServicesManage)


admin.site.register(NewsCategory)
admin.site.register(RepairStatus)

admin.site.register(Sections)
admin.site.register(Compliment)
admin.site.register(CallToAction)
admin.site.register(PhotoHeaderHomePage)
admin.site.register(IconAds)
admin.site.register(FontAweasom)
admin.site.register(Doctor)
admin.site.register(ProfileUser)
admin.site.register(ProgramOffice)
admin.site.register(ServiceArtical)
admin.site.register(ConferenceSchedule)
admin.site.register(LinkExternal)
admin.site.register(Cyber_Alert)
admin.site.register(OnePage)
admin.site.register(ITWebBlog)
admin.site.register(ComBranding)
admin.site.register(jobposition)
admin.site.register(BorrowDevice)
admin.site.register(FormerUser)


class ComputerAccessoryManage(admin.ModelAdmin):
	list_display = ["date","comphoto","comtype","combranding","deviceID","owner","section"]
	list_editable = ["comphoto","comtype","combranding","deviceID","owner","section"]
	list_per_page = 4
	
	list_filter = ["comtype","combranding","section"]

admin.site.register(ComputerAccessory,ComputerAccessoryManage)
admin.site.register(PhotoComputerAccessory)

		

class ComdealerManage(admin.ModelAdmin):
	list_display = ["dealername","dealer_addr","tel"]
	
	list_per_page = 4

admin.site.register(Comdealer,ComdealerManage)
#admin.site.register(Comdealer)


admin.site.register(ProjectBudget)
admin.site.register(PartsFromRepairBookMemory)
admin.site.register(RepairBookMemory)

admin.site.register(ComputerType)

class RepairManage(admin.ModelAdmin):
	list_display = ["owner","repaircase"]
	
	list_per_page = 4

admin.site.register(RepairAndPartChange,RepairManage)



class ComrequestManage(admin.ModelAdmin):
	list_display = ["date","user","request","comtype"]
	list_editable = ["user","request","comtype"]
	list_per_page = 4
admin.site.register(ComRequest,ComrequestManage)


#อัพโหลดเพื่อโหลดไฟล์

class FileDownloadManage(admin.ModelAdmin):
	list_display = ["postdate","title","file","section","category","user"]
	list_editable = ["title","file","section","category","user"]
	list_per_page = 4

admin.site.register(FileDownload,FileDownloadManage)















# Register your models here.
