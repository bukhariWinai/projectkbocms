
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


@login_required	
def ServerMainten(request):
	

			#resolve_item = SerVerMainten.objects.all()
		
		
			if request.user.profileuser.usergroup == 'admin' or 'trainee':	

					if request.method == 'POST':
					
				# create object of form SerVerMaintenForm
						serverdiagform = SerVerMaintenForm(request.POST)

						photo = request.FILES.getlist("img_case") #field comphoto มากจาก feild เก็บค่า imagefeild ในฐานข้อมูล

						if serverdiagform.is_valid():
							serverdiagform.instance.user = request.user.profileuser
							
							f = serverdiagform.save(commit=False)

							f.save()

							for img in photo:
								ImageServerRepair.objects.create(case_id=f,img_case=img)

								messages.success(request,"บันทึกการแก้ใขเครื่อง SERVER เรียบร้อยแล้ว ")
								return redirect('servermainten_page')
						else:
						#messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
							return render(request, "server_mainten/servermainten.html",{'serverdiagform': serverdiagform } )

					
					context = {'serverdiagform': SerVerMaintenForm(),}

					return render(request, "server_mainten/servermainten.html", context)

			else:	
				return redirect('servermainten_page')

@login_required		
def AddSerVer(request):
	
			if request.user.profileuser.usergroup == 'admin' or 'trainee':	

					if request.method == 'POST':
					
				# create object of form SerVerMaintenForm
						serverform = addSerVerForm(request.POST)

						photo = request.FILES.getlist("img_server") #field comphoto มากจาก feild เก็บค่า imagefeild ในฐานข้อมูล

						if serverform.is_valid():
							serverform.instance.user = request.user.profileuser		
														
							f = serverform.save(commit=False)

							f.save()

							for img in photo:
								ImageServer.objects.create(server_id=f,img_server=img)

								messages.success(request,"บันทึกเครื่อง SERVER เรียบร้อยแล้ว ")
						
						else:
							messages.warning(request,"กรุณาตรวจสอบหมายเลขครุภัณฑ์")
							return render(request, "server_mainten/addserver.html",{'serverform': serverform } )

					
					context = {'serverform': addSerVerForm(),}

					return render(request, "server_mainten/addserver.html", context)

			else:	
				return redirect('addserver_page')
	

@login_required	
def ItemServerMainten(request):
	item_mainten =  SerVerMainten.objects.all().reverse()

	context = {'item_mainten':item_mainten}
	return render(request, 'server_mainten/itemservermainten.html',context )
@login_required	
def ServerMaintenDetails(request,mainten_id):
	comdetail = get_object_or_404(SerVerMainten,id=mainten_id) 
	comphoto = ImageServerRepair.objects.filter(case_id=mainten_id) 
	
	context = {'comdetail':comdetail,'comphoto':comphoto}
	return render(request, 'server_mainten/servermaintendetails.html', context)	