from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import HttpResponse, render, redirect
from .models import *
from .forms import *
from django.db.models import Q


# ต้องมีโมเดล setting เพื่อกำหนดค่าทั่วไปชองเว็บไซต์ เช่น ซื่อเว็บ ชื่อหน่วยงาน ลิงค์ u tube ประชาสัมพันธ์ต่างๆ

def Home(request):

	All_news = News.objects.all().order_by("date").reverse()[:12]
	aboutus = AboutUs.objects.all().order_by("id").reverse()[:1]
	newssec1 = News.objects.filter(category=1) #category=1  ข่าวกลุ่มงาน 
	newssec2 = News.objects.filter(category=2) #category=2  ข่าวประชาสัมพันธ์
	newssec3 = News.objects.filter(category=3) #category=3  ข่าวบริการ
	newssec4 = FileDownload.objects.filter(category_id=5) #category=5  ข่าวจัดซื้อจัดจ้าง
	health_artical = News.objects.filter(category=12).order_by("id").reverse()[:1] #category=4  [บทความสุขภาพ]

	trophy = Compliment.objects.all()
	ca = CallToAction.objects.all()
	os = OurServices.objects.all()
	pt = PhotoHeaderHomePage.objects.all().order_by("id").reverse()[:1]
	icon = IconAds.objects.all().reverse()
	dr = Doctor.objects.all().order_by("id").reverse()[:9]
	linkext1 = LinkExternal.objects.all()[:7]
	linkext2 = LinkExternal.objects.all()[6:]


	title = 'สำนักงานสาธารณสุขจังหวัดกระบี่'
	motto = 'คนกระบี่สุขภาพดี เจ้าหน้าที่ความสุข ระบบสุขภาพได้คุณภาพ'
	youtube = 'https://www.youtube.com/watch?v=6KhNdR2ke4k' #youtube headerpage


	context = {
				'title':title,
				'motto':motto,
				'youtube':youtube,
				'linkext1':linkext1,
				'linkext2':linkext2,	

				'All_news':All_news,
				'aboutus':aboutus,
				'newssec1':newssec1,
				'newssec2':newssec2,
				'newssec3':newssec3,
				'newssec4':newssec4,
				'health_artical':health_artical,
				'trophy':trophy,
				'ca':ca,
				'os':os,
				
				'pt':pt,
				'icon':icon,
				'dr':dr,
				}

	return render(request,'cmsapp/home.html',context)
	

def NewsShow(request):

	All_news = News.objects.all().order_by("date").reverse()[:12]

	paginator = Paginator(All_news,9)
	page = request.GET.get('page')
	All_news = paginator.get_page(page)

	context = {'All_news':All_news}
	return render (request,'cmsapp/news.html',context)

def OnePages(request):

	All_onepage = OnePage.objects.all().order_by("postdate").reverse()
	paginator = Paginator(All_onepage,9)
	page = request.GET.get('page')
	All_onepage = paginator.get_page(page)

	context = {'All_onepage':All_onepage}
	return render (request,'cmsapp/onepages.html',context)

def OnePageDetail(request,op_id):
	onepage = OnePage.objects.get(id=op_id)


	context = {'onepage':onepage}
	return render (request,'cmsapp/onepagedetail.html',context)


def PostDetails(request,serviceid):

	service = OurServices.objects.get(id=serviceid)
	lastnews = News.objects.all().order_by('id').reverse()[:2]
	
	context = {
				'service':service,
				'lastnews': lastnews,
				}
	
	return render(request,'cmsapp/post-details.html',context)

def DocDetails(request,doc_id):

	docdetail = FileDownload.objects.get(id=doc_id)
	
	context = {
				'docdetail':docdetail,
				}
	
	return render(request,'cmsapp/document-details.html',context)


def ProgramOfficeView(request):

	link = ProgramOffice.objects.all()
	
	context = {'link':link}


	return render(request,'cmsapp/officecenter.html',context)


def NewsDetails(request,news_id): #new

	lastnews = News.objects.all().order_by('id').reverse()[:4]
	news_photos = NewsPhoto.objects.filter(news_id_id=news_id)
	#print(news_photo)
	newsdetail = News.objects.get(id=news_id) #new
	context = {'newsdetail':newsdetail,
				'lastnews':lastnews,
				'news_photos':news_photos,
				
				}
	
	return render(request,'cmsapp/news-details.html',context)

def ItAdmin(request):
	
	return render(request,'cmsapp/itadmin_page.html',context)


def Anounce(request):
	return render(request,'cmsapp/anounce.html')

def Contact(request):
	return render(request,'cmsapp/contact.html')



def Download(request):
    q = request.GET.get('q', '').strip()            # คำค้น
    category_id = request.GET.get('category')       # id จาก dropdown

    downloads = FileDownload.objects.all().order_by('-postdate')

    # ค้นหา text
    if q:
        downloads = downloads.filter(
            Q(title__icontains=q) | 
            Q(section__sectionsname__icontains=q) | 
            Q(user__user_id__first_name__icontains=q) |
            Q(user__user_id__last_name__icontains=q)
        )

    # กรองตาม category ถ้ามี
    if category_id and category_id.isdigit():
        downloads = downloads.filter(category_id=int(category_id))

    # Pagination
    paginator = Paginator(downloads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ดึงข้อมูล category ทั้งหมด สำหรับ dropdown
    categories = NewsCategory.objects.all()

    context = {
        'download': page_obj,
        'categories': categories,     # ส่งไป template
        'q': q,
        'category_id': category_id,
        'total_results': downloads.count()
    }

    return render(request, 'cmsapp/download.html', context)


def FormDownload(request):
    q = request.GET.get('q', '').strip()            # คำค้น
    category_id = request.GET.get('category')       # id จาก dropdown

    downloads = FileDownload.objects.all().order_by('-postdate')

    # ค้นหา text
    if q:
        downloads = downloads.filter(
            Q(title__icontains=q) | 
            Q(section__sectionsname__icontains=q) | 
            Q(user__user_id__first_name__icontains=q) |
            Q(user__user_id__last_name__icontains=q)
        )

    # กรองตาม category ถ้ามี
    if category_id and category_id.isdigit():
        downloads = downloads.filter(category_id=int(category_id))

    # Pagination
    paginator = Paginator(downloads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ดึงข้อมูล category ทั้งหมด สำหรับ dropdown
    categories = NewsCategory.objects.all()

    context = {
        'download': page_obj,
        'categories': categories,     # ส่งไป template
        'q': q,
        'category_id': category_id,
        'total_results': downloads.count()
    }

    return render(request, 'cmsapp/formdownload.html', context)



def Promote(request):

	newspromote = News.objects.filter(category__id=3).order_by("date").reverse()
	context = {'newspromote':newspromote}
	return render(request,'cmsapp/promote.html',context)

def Section(request):
	sect = Sections.objects.all()
	context = {'sect':sect,}

	return render(request,'cmsapp/section.html',context)

def Services(request):

	service = OurServices.objects.all()
	context = {'service':service,}
	
	return render(request,'cmsapp/services.html',context)

def Comrequest(request):

	artical = ServiceArtical.objects.all().reverse()[:10]

	reqcom = ComRequest.objects.all().reverse()[:10]

	context = {'reqcom':reqcom,'artical':artical}

	return render(request,'cmsapp/comrequest.html',context)


def CyberPolicy(request):

	cyberalert = Cyber_Alert.objects.all().order_by('date').reverse()[:5]
	itwebblog = ITWebBlog.objects.all().order_by('id')
	context = {
				'cyberalert':cyberalert ,
				'itwebblog':itwebblog ,
				}

	return render(request,'cmsapp/cyber_policy.html',context)

def CyberPolicyDetail(request,policyid):

	itwebblog = ITWebBlog.objects.get(id=policyid)
	
	context = {
				'itwebblog':itwebblog ,
				
				}


	return render(request,'cmsapp/policy_detail.html',context)


def CyberImpectDetail(request,cyberimpectid):

	cyberimpect = Cyber_Alert.objects.get(id=cyberimpectid)
	context = { 'cyberimpect':cyberimpect

				}

	return render(request,'cmsapp/cyberimpectdetail.html',context)


def ConferenceView(request):
    q = request.GET.get('q', '').strip()   # รับค่าค้นหา

    conf = ConferenceSchedule.objects.all().order_by('-id')

    # ถ้ามีการค้นหา
    if q:
        conf = conf.filter(Q(title__icontains=q))

    # Pagination
    paginator = Paginator(conf, 10)  # แสดง 10 รายการต่อหน้า
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'conf': page_obj,
        'q': q,
    }
    return render(request, 'cmsapp/conference.html', context)


def ConfScheduleView(request,confid):

	confdetails = ConferenceSchedule.objects.get(id=confid)

	context = {'confdetails':confdetails,}

	return render(request,'cmsapp/confschedule_page.html',context)


def AddNewsForm(request):
		lastnews = News.objects.all().order_by('id').reverse()[:2]

		if request.method == 'POST':
			
		# create object of form
			form = NewsForm(request.POST or None, request.FILES or None)
		
		# check if form data is valid
			if form.is_valid():
				
				title = form.cleaned_data['title']
				post = form.cleaned_data['post']
				#cleaned_da = form.cleaned_data
				# save the form data to model
				form.save()
				messages.success(request,"ถูกต้อง/ลงข่าวเรียบร้อยแล้ว ")
				#return HttpResponseRedirect('addnewsform.html')
			else:
				messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
				return render(request, "cmsapp/addnewsform.html",{'form':form} )

		context = {	'form':NewsForm(),'lastnews':lastnews,}			
		return render(request, "cmsapp/addnewsform.html", context)

		
	
	
	

	#return render(request, "cmsapp/addnewsform.html", context)	




'''
def Login(request):
	return render(request,'cmsapp/login.html')
'''
# Create your views here.
