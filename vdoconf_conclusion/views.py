
from django.shortcuts import render, get_object_or_404,HttpResponse,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages

from cmsapp.models import * #นำโมเดล model จาก cmsapp มาใช้งาน
from .forms import * 
from django.db.models import Sum,Count,Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,FormView
from django.urls import reverse
from cmsapp_backend.models import * #นำโมเดล model จาก cmsapp_backend มาใช้งาน
from server_mainten.models import * #นำโมเดล model จาก cmsapp_backend มาใช้งาน



# Create your views here.
@login_required	
def Homeconf(request):

	if request.user.profileuser.usergroup == 'admin' or 'trainee':	

					if request.method == 'POST':
					
				# create object of form vdoconf_conclusion
						vdoconf_form = VdoconfConclusionForm(request.POST)

						photo = request.FILES.getlist("img_vdoconf") #field comphoto มากจาก feild เก็บค่า imagefeild ในฐานข้อมูล

						if vdoconf_form.is_valid():
							vdoconf_form.instance.user = request.user.profileuser
							
							f = vdoconf_form.save(commit=False)

							f.save()

							for img in photo:
								ImageConf.objects.create(vdoconf_id=f,img_vdoconf=img)

								messages.success(request,"บันทึกการแก้ใขเครื่อง SERVER เรียบร้อยแล้ว ")
						
						else:
						#messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
							return render(request, "vdoconf_conclusion/homeconf.html",{'vdoconf_form': vdoconf_form } )

					
					context = {'vdoconf_form': VdoconfConclusionForm(),}

					return render(request, "vdoconf_conclusion/homeconf.html", context)

	


@login_required	
def Allconf(request):
	allconf =  VdoconfConclusion.objects.all().reverse()

	context = {'allconf':allconf}
	return render(request, 'vdoconf_conclusion/allconf.html',context )
@login_required	
def ConfDetails(request,conf_id):
	confdetail = get_object_or_404(VdoconfConclusion,id=conf_id) 
	comphoto = ImageConf.objects.filter(vdoconf_id=conf_id) 
	
	context = {'confdetail':confdetail,'comphoto':comphoto}
	return render(request, 'vdoconf_conclusion/confdetails.html', context)	