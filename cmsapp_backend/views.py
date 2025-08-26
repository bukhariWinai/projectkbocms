from django.shortcuts import render, get_object_or_404,HttpResponse,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from cmsapp.models import * #นำโมเดล model จาก cmsapp มาใช้งาน
from .forms import * 
from django.db.models import Sum,Count,Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,FormView
from django.urls import reverse
from django.db import transaction
from cmsapp_backend.models import * #นำโมเดล model จาก cmsapp_backend มาใช้งาน
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import qrcode
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
from cmsapp_backend.utils.alerts import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import mm
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter
from django.utils.html import strip_tags
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from textwrap import wrap
from django.http import JsonResponse
from sparepart.models import PartsSubCatName
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# ตำแหน่งที่เก็บไฟล์ฟอนต์
   
@login_required
@never_cache

def ShowAllDevices(request):

	Com = ComputerAccessory.objects.annotate(repair_count=Count('repairs')).order_by('id')
	context = {'Com':Com,}
	return render(request, 'cmsapp_backend/showalldevices.html', context)

@login_required
@never_cache
def ShowDeviceRepair(request,showrepaired_id):

	showdeviceRepaired = RepairAndPartChange.objects.filter(hw_id=showrepaired_id)
	print(showdeviceRepaired)

	context = {'showdeviceRepaired':showdeviceRepaired,}
	return render(request, 'cmsapp_backend/showdevicerepair.html', context)

@login_required
@never_cache
def ComputerDetails(request,com_id):
	comdetail = get_object_or_404(ComputerAccessory,id=com_id) 
	comphoto = PhotoComputerAccessory.objects.filter(hw_number_id=com_id)
	add_former = AddFormerUserForm(instance=comdetail) # โชว์ ข้อมูลใน textfield เพื่อการแก้ใขต่าง ใช้งานร่วมกับ context ด้านล่าง บรรทัด 53
	user_former = FormerUser.objects.filter(id_com_id=com_id)
	
	if request.method == 'POST':
		# Initialize form with POST data and files
		form = AddFormerUserForm(request.POST or None, request.FILES or None,instance=comdetail)
		
		if form.is_valid():
			#instance = form.save()
			former_user = form.cleaned_data['former_user']
			date_return = form.cleaned_data['date_return']						
			FormerUser.objects.create(id_com=comdetail,former_user=former_user,date_return=date_return)
			#form.save()
			messages.success(request,"บันทึกสำเร็จ")
			#return redirect('update_success_page')  # Replace with your success URL name
			return redirect('computerdetails_page', com_id=com_id)
		else:
			
			# Return invalid form with error
			return render(request, "cmsapp_backend/computerdetails.html", {'form': form})
	
	else:
		# GET request, initialize empty form

		form = AddFormerUserForm()
	
	context = {'comdetail':comdetail,'comphoto':comphoto,'form': form,'user_former':user_former} #'user_fomer':user_fomer
	return render(request, 'cmsapp_backend/computerdetails.html', context)	
	
@login_required	
@never_cache
def ComputerUpdateDetails(request,item_id):
	comdetail = get_object_or_404(ComputerAccessory,id=item_id)
	ComUpdate = FormComputerUpdateDetails(instance=comdetail) # โชว์ ข้อมูลใน textfield เพื่อการแก้ใขต่าง ใช้งานร่วมกับ context ด้านล่าง บรรทัด 53
	
	if request.user.profileuser.usergroup == 'admin' :	

				if request.method == 'POST':

					ComUpdate = FormComputerUpdateDetails(request.POST or None, request.FILES or None,instance=comdetail)
				
				# check if form data is valid
					if ComUpdate.is_valid():

						#formComp.instance.owner = request.user.profileuser										
						ComUpdate.save()
						
						messages.success(request,"บันทึกเรียบร้อยแล้ว ")
												
					else:
						
						messages.warning(request,"ลองใหม่อีกครั้ง")						

				context = {'ComUpdate': ComUpdate,'comdetail': comdetail,}
				return render(request,'cmsapp_backend/computerupdatedetails.html',context)

	else:	
		return redirect('showalldevices_page')

@login_required
@never_cache
def Generate_Qr_Pdf(request, cp_id):
	# สร้างข้อมูลที่ต้องการใส่ใน QR
	data_device = ComputerAccessory.objects.get(id=cp_id)
	LABEL_WIDTH = 283
	LABEL_HEIGHT = 150
	qr_data = request.build_absolute_uri(f"/computerdetails/{cp_id}/ComputerDetails/")

	# สร้าง QR Code
	qr_img = qrcode.make(qr_data)  # PIL Image

	# บันทึก QR Image ลงใน BytesIO (จำลองเป็นไฟล์ภาพ)
	qr_buffer = BytesIO()
	qr_img.save(qr_buffer, format='PNG')
	qr_buffer.seek(0)

	# ใช้ ImageReader เพื่อให้ PDF อ่านภาพได้
	qr_image = ImageReader(qr_buffer)

	# ===== Register THSarabun Fonts =====
	font_dir = os.path.join(settings.BASE_DIR, 'cmsapp_backend', 'fonts')
	font_path = os.path.join(font_dir, 'THSarabun.ttf')
	bold_font_path = os.path.join(font_dir, 'THSarabun Bold.ttf')
	if not os.path.exists(font_path) or not os.path.exists(bold_font_path):
		return HttpResponse("ไม่พบไฟล์ฟอนต์ THSarabun", status=500)

	pdfmetrics.registerFont(TTFont('THSarabun', font_path))
	pdfmetrics.registerFont(TTFont('THSarabun-Bold', bold_font_path))
	registerFontFamily('THSarabun', normal='THSarabun', bold='THSarabun-Bold')
	

	# สร้าง PDF
	pdf_buffer = BytesIO()
	p = canvas.Canvas(pdf_buffer, pagesize=(LABEL_WIDTH, LABEL_HEIGHT))
	p.setTitle("KBOCMS-computer_label")

	# วาดโลโก้สำนักงานสาธารณสุขจังหวัดกระบี่
	# logo_path = 'media/ImageUserProfile/cropped-LOGO-2.png'  # เปลี่ยนเป็น path ที่ถูกต้อง localhost
	logo_path = os.path.join(settings.MEDIA_ROOT, 'ImageUserProfile/cropped-LOGO-2.png') 
	p.drawImage(logo_path, x=10, y=LABEL_HEIGHT - 35, width=20, height=20,mask='auto')  # วางโลโก้ที่มุมซ้ายบน

	# ใส่ข้อมูลข้อความ
	p.setFont("THSarabun", 16)  # ฟอนต์รองรับไทย
	y = 120
	p.drawString(35, y, f"Krabi Provincial Health Public Office")
	y -= 25
	p.drawString(12, y, f"ผู้ใช้: {data_device.owner}")
	y -= 15
	p.drawString(12, y, f"กลุ่มงาน: {data_device.section}")
	y -= 15
	p.drawString(12, y, f"รหัสครุภัณฑ์: {data_device.deviceID}")
	y -= 15
	p.drawString(12, y, f"Brand: {data_device.combranding}")
	y -= 15
	p.drawString(12, y, f"Model: {data_device.commodel}")
	y -= 15
	p.drawString(12, y, f"S/N: {data_device.comserailnumber}")
	
	# วาด QR ลง PDF ด้วย ImageReader
	p.drawImage(qr_image, x=200, y=35, width=70, height=70)

	p.showPage()
	p.save()
	pdf_buffer.seek(0)

	# ส่งไฟล์ PDF
	response = HttpResponse(pdf_buffer, content_type='application/pdf')
  
	return response


@login_required
@never_cache
def Generate_UserProfile_Pdf(request, user_id):
	# ดึงข้อมูลผู้ใช้จาก user_id
	profile = ProfileUser.objects.get(id=user_id)

	# ขนาดกระดาษลาเบล (100mm x 75mm)
	LABEL_WIDTH = 100 * mm
	LABEL_HEIGHT = 75 * mm
	page_size = (LABEL_WIDTH, LABEL_HEIGHT)

	# สร้าง HttpResponse เป็นไฟล์ PDF
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="KBOCMS-printuser.pdf"'
	# response['Content-Disposition'] = f'inline; filename="user_{user_id}_label.pdf"'

	# ===== Register THSarabun Fonts =====
	font_dir = os.path.join(settings.BASE_DIR, 'cmsapp_backend', 'fonts')
	font_path = os.path.join(font_dir, 'THSarabun.ttf')
	bold_font_path = os.path.join(font_dir, 'THSarabun Bold.ttf')
	if not os.path.exists(font_path) or not os.path.exists(bold_font_path):
		return HttpResponse("ไม่พบไฟล์ฟอนต์ THSarabun", status=500)

	pdfmetrics.registerFont(TTFont('THSarabun', font_path))
	pdfmetrics.registerFont(TTFont('THSarabun-Bold', bold_font_path))
	registerFontFamily('THSarabun', normal='THSarabun', bold='THSarabun-Bold')

	# สร้าง Canvas
	p = canvas.Canvas(response, pagesize=page_size)
	p.setTitle("KBOCMS-printuser")
	p.setFont("THSarabun", 22)

	# เพิ่มโลโก้
	logo_path = os.path.join(settings.MEDIA_ROOT, 'ImageUserProfile/cropped-LOGO-2.png')
	if os.path.exists(logo_path):
		p.drawImage(logo_path, x=20, y=LABEL_HEIGHT - 35, width=25, height=25, mask='auto')

	# เพิ่มข้อมูลผู้ใช้ลงในลาเบล
	p.drawString(50, LABEL_HEIGHT - 30, f" สำนักงานสาธารณสุขจังหวัดกระบี่ ")
	p.drawString(40, LABEL_HEIGHT - 60, f"ชื่อ: {profile.user.first_name}  {profile.user.last_name[:4]}********")
	p.drawString(40, LABEL_HEIGHT - 80, f"Username: {profile.user.username}")
	p.drawString(40, LABEL_HEIGHT - 100, f"Password:  *************")
	p.drawString(40, LABEL_HEIGHT - 140, f"โปรดเก็บ Username และ Password ")
	p.drawString(40, LABEL_HEIGHT - 160, f"เป็นความลับ !")
	
	# บันทึกและแสดงผล
	p.showPage()
	p.save()
	return response

@login_required
@never_cache
def ExportConsentPdf(request, cp_id):
	accessory = ComputerAccessory.objects.get(id=cp_id)
	owner = accessory.owner

	# สร้าง HttpResponse ที่มีประเภทเป็น PDF
	response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = f'attachment; filename="consent_form_{owner.user.username}.pdf"'

	# สร้าง canvas ของ PDF
	# p.setTitle("KBOCMS-แบบฟอร์มยืมครุภัณฑ์คอมพิวเตอร์")
	p = canvas.Canvas(response)
	p.setTitle("KBOCMS-แบบฟอร์มยืมครุภัณฑ์คอมพิวเตอร์")

	# ===== Register THSarabun Fonts =====
	font_dir = os.path.join(settings.BASE_DIR, 'cmsapp_backend', 'fonts')
	font_path = os.path.join(font_dir, 'THSarabun.ttf')
	bold_font_path = os.path.join(font_dir, 'THSarabun Bold.ttf')

	if not os.path.exists(font_path) or not os.path.exists(bold_font_path):
		return HttpResponse("ไม่พบไฟล์ฟอนต์ THSarabun", status=500)

	pdfmetrics.registerFont(TTFont('THSarabun', font_path))
	pdfmetrics.registerFont(TTFont('THSarabun-Bold', bold_font_path))
	registerFontFamily('THSarabun', normal='THSarabun', bold='THSarabun-Bold')

	# เนื้อหาฟอร์ม
	p.setFont("THSarabun-Bold", 22)
	p.drawString(160, 760, "แบบฟอร์มยืมครุภัณฑ์คอมพิวเตอร์เพื่อการปฏิบัติงานราชการ")

	p.setFont("THSarabun", 16)
	p.drawString(100, 720, f"ชื่อผู้ใช้: {owner.user.first_name} {owner.user.last_name}")
	p.drawString(100, 700, f"ตำแหน่ง: {getattr(owner, 'jobposition_name',)}")
	p.drawString(100, 680, f"หน่วยงาน: {accessory.section }")
	p.drawString(100, 660, f"รหัสครุภัณฑ์: {accessory.deviceID or '-'}")
	p.drawString(100, 640, f"ยี่ห้อ / รุ่น: {accessory.combranding} / {accessory.commodel or '-'}")
	p.drawString(100, 620, f"คุณลักษณะครุภัณฑ์: {accessory.comspec} ")

	# ช่องว่างให้ลงชื่อ
	p.drawString(130, 580, "ข้าพเจ้ามีความประสงค์ขอรับครุภัณฑ์นี้ซึ่งเป็นทรัพย์สินทางราชการ เพื่อใช้ในการปฎิบัติงานของทางราชการ ")    
	p.drawString(100, 560, "จะดูแลรักษาครุภัณฑ์นี้ให้อยู่ในสภาพดีพร้อมใช้งาน และจะคืนกับหัวหน้าส่วนราชการเมื่อไม่มีความจำเป็นต้องใช้")
	p.drawString(100, 540, "งานต่อไป")
	p.drawString(300, 510, "ลงชื่อ.....................................................ผู้รับครุภัณฑ์ ")    
	p.drawString(340, 490, f" ({owner.user.first_name} {owner.user.last_name})")
	p.drawString(320, 470, f"  วันที่รับ.................................... ")

	p.drawString(300, 410, "ลงชื่อ.....................................................ผู้ส่งมอบ ")    
	p.drawString(320, 390, f" (.....................................................)")
	p.drawString(300, 370, f"  วันที่ส่งมอบ.......................................... ")

	p.showPage()
	p.save()

	return response

@login_required
@never_cache
def ExportWorkReportPdf(request, wr_id):
	try:
		report = DailyWorkReport.objects.get(id=wr_id)
		trainee = report.usertrinee
		admin = report.admin_control
	except DailyWorkReport.DoesNotExist:
		return HttpResponse("ไม่พบรายงานการทำงาน", status=404)

	# ===== Register THSarabun Fonts =====
	font_dir = os.path.join(settings.BASE_DIR, 'cmsapp_backend', 'fonts')
	font_path = os.path.join(font_dir, 'THSarabun.ttf')
	bold_font_path = os.path.join(font_dir, 'THSarabun Bold.ttf')

	if not os.path.exists(font_path) or not os.path.exists(bold_font_path):
		return HttpResponse("ไม่พบไฟล์ฟอนต์ THSarabun", status=500)

	pdfmetrics.registerFont(TTFont('THSarabun', font_path))
	pdfmetrics.registerFont(TTFont('THSarabun-Bold', bold_font_path))
	registerFontFamily('THSarabun', normal='THSarabun', bold='THSarabun-Bold')

	buffer = BytesIO()
	p = canvas.Canvas(buffer, pagesize=A4)
	p.setTitle("KBOCMS@trainee-แบบฟอร์มรายงานการปฏิบัติงานประจำวันนักศึกษาฝึกงาน")

	width, height = A4

	def draw_footer_with_page(p):
		p.setFont("THSarabun", 14)
		p.setFillColor(colors.gray)
		p.drawString(2 * cm, 2 * cm, "KBOCMS_MODULE @trainee by DevBukhari")

	# ===== Header =====os.path.join(settings.MEDIA_ROOT, 'media/ImageUserProfile/cropped-LOGO-2.png') 
	logo_path = os.path.join(settings.MEDIA_ROOT, 'ImageUserProfile/cropped-LOGO-2.png') 
	if os.path.exists(logo_path):
		p.drawImage(logo_path, 2 * cm, height -8 * cm, width=2*cm, preserveAspectRatio=True, mask='auto')

	p.setFont("THSarabun-Bold", 22)
	p.setFillColor(colors.HexColor('#003366'))
	p.drawString(4.5 * cm, height - 2.5 * cm, "รายงานการปฏิบัติงานประจำวัน กลุ่มงานสุขภาพดิจิทัล สสจ.กระบี่")

	p.setFont("THSarabun", 16)
	p.setFillColor(colors.black)
	p.drawString(4.5 * cm, height - 3.2 * cm, "ระบบ KBOCMS – ระบบติดตามนักศึกษาฝึกงาน")

	p.setStrokeColor(colors.lightgrey)
	p.setLineWidth(0.5)
	p.line(2 * cm, height - 4.2 * cm, width - 2 * cm, height - 4.2 * cm)
	p.setStrokeColor(colors.lightgrey)
	p.setLineWidth(0.5)
	p.line(2 * cm, height - 5.2 * cm, width - 2 * cm, height - 5.2 * cm)

	p.setFont("THSarabun-Bold", 18)
	p.setFillColor(colors.gray)
	p.drawString(2 * cm, height - 4.8 * cm, f"วันที่รายงาน: {report.date.strftime('%d/%m/%Y %H:%M')}")

	y = height - 6 * cm
	line_height = 1 * cm

	def draw_line(label, value):
		nonlocal y
		p.setFont("THSarabun-Bold", 18)
		p.setFillColor(colors.black)
		p.drawString(2 * cm, y, f"{label}:")
		p.drawString(9 * cm, y, str(value))
		y -= line_height

	draw_line("ชื่อนักศึกษา", trainee.user.get_full_name() if trainee else "N/A")
	draw_line("เลขที่ใบงาน", report.id or "-")
	draw_line("ใบงาน", report.workitem or "-")
	draw_line("คะแนนการประเมิน(เต็ม 5 คะแนน)", report.rating if report.rating is not None else "-")
	draw_line("ผลการประเมิน", "ผ่าน" if report.result else "ไม่ผ่าน")
	
	p.setStrokeColor(colors.lightgrey)
	p.setLineWidth(0.5)
	p.line(2 * cm, height - 12 * cm, width - 2 * cm, height - 12 * cm)

	p.setStrokeColor(colors.lightgrey)
	p.setLineWidth(0.5)
	p.line(2 * cm, height - 11 * cm, width - 2 * cm, height - 11 * cm)

	# ===== รายละเอียดงาน =====
	y -= 0.5 * cm
	p.setFont("THSarabun-Bold", 16)
	p.drawString(2 * cm, y, "รายละเอียดงาน:")
	y -= line_height
	p.setFont("THSarabun", 16)

	work_text = strip_tags(report.workdisc or "ไม่มีรายละเอียด")
	max_chars = 90
	for line in work_text.splitlines():
		for subline in wrap(line, width=max_chars):
			p.drawString(2.5 * cm, y, subline)
			y -= 0.8 * cm
			if y < 3 * cm:
				draw_footer_with_page(p)
				p.showPage()
				y = height - 3 * cm
				p.setFont("THSarabun", 16)

	# ===== รูปภาพประกอบ =====
	image_qs = ImagesCloud.objects.filter(workid=report)
	if image_qs.exists():
		draw_footer_with_page(p)
		p.showPage()
		y = height - 3 * cm
		p.setFont("THSarabun-Bold", 16)
		p.drawString(2 * cm, y, f"ภาพประกอบการทำงาน ใบงานที่ ({report.id}) : {report.workitem or '-'}" )
		y -= 1.5 * cm

		for img in image_qs:
			image_path = os.path.join(settings.MEDIA_ROOT, str(img.images))
			if os.path.exists(image_path):
				try:
					p.drawImage(image_path, 2 * cm, y - 6 * cm, width=10 * cm, height=6 * cm, preserveAspectRatio=True, mask='auto')
					y -= 7 * cm
					if y < 7 * cm:
						draw_footer_with_page(p)
						p.showPage()
						y = height - 3 * cm
				except Exception as e:
					p.drawString(2 * cm, y, f"แสดงภาพไม่สำเร็จ: {str(e)}")
					y -= 1 * cm

	# ===== หมายเหตุ และผู้ควบคุม =====
	def draw_line_remark(label, value):
		nonlocal y
		p.setFont("THSarabun-Bold", 18)
		p.setFillColor(colors.black)
		p.drawString(2 * cm, y, f"{label}:")
		p.setFont("THSarabun", 16)
		p.drawString(4 * cm, y, str(value))
		y -= line_height

	remark_text = strip_tags(report.remark or "")
	draw_line_remark("หมายเหตุ", remark_text or "-")
	

	# ===== ลายเซ็น =====
	if y < 6 * cm:
		draw_footer_with_page(p)
		p.showPage()
		y = height - 3 * cm

	y -= 2 * cm
	p.setFont("THSarabun", 16)
	p.drawString(2 * cm, y, "ลงชื่อ ..........................................................")
	p.drawString(4 * cm, y - 1 * cm, f"( {admin.user.get_full_name() if admin else ''} )")
	p.drawString(3.5 * cm, y - 2 * cm, "ผู้ควบคุมการฝึกงาน")

	# ===== QR Code =====
	qr_url = request.build_absolute_uri(f"/export_workreport/{wr_id}/pdf")
	qr = qrcode.make(qr_url)
	qr_io = BytesIO()
	qr.save(qr_io, format='PNG')
	qr_io.seek(0)
	p.drawImage(ImageReader(qr_io), 2 * cm, y - 5 * cm, width=2 * cm, height=2 * cm)

	p.setFont("THSarabun", 11)
	p.drawString(2.2 * cm, y - 5.1 * cm, f"( {trainee.user.get_full_name() if trainee else ''} )")
	p.setFont("THSarabun", 12)
	p.drawString(2 * cm, y - 5.5 * cm, "สแกน QR Code เพื่อดูรายงานออนไลน์")

	draw_footer_with_page(p)
	p.showPage()
	p.save()
	buffer.seek(0)

	# ===== ใส่เลขหน้า =====
	reader = PdfReader(buffer)
	writer = PdfWriter()
	total_pages = len(reader.pages)

	for i, page in enumerate(reader.pages):
		packet = BytesIO()
		c = canvas.Canvas(packet, pagesize=A4)
		c.setFont("THSarabun", 14)
		c.setFillColor(colors.gray)
		c.drawCentredString(width - 80, 2 * cm, f"หน้าที่ {i + 1} / {total_pages}")
		c.save()
		packet.seek(0)
		overlay = PdfReader(packet)
		page.merge_page(overlay.pages[0])
		writer.add_page(page)

	final_buffer = BytesIO()
	writer.write(final_buffer)
	final_buffer.seek(0)

	response = HttpResponse(final_buffer, content_type='application/pdf')
	response['Content-Disposition'] = f'inline; filename="workreport_{trainee.user.username}.pdf"'
	return response

@login_required
@never_cache
def ExportReturnDevicePdf(request, cp_id):
	accessory = ComputerAccessory.objects.get(id=cp_id)
	owner = accessory.owner

	# สร้าง HttpResponse ที่มีประเภทเป็น PDF
	response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = f'attachment; filename="consent_form_{owner.user.username}.pdf"'

	# สร้าง canvas ของ PDF
	p = canvas.Canvas(response)
	p.setTitle("KBOCMS-แบบฟอร์มคืนครุภัณฑ์คอมพิวเตอร์")


	# เนื้อหาฟอร์ม
	p.setFont("THSarabun", 20)
	p.drawString(160, 760, "แบบฟอร์ม ขอคืนครุภัณฑ์คอมพิวเตอร์เพื่อการปฏิบัติงานราชการ")

	p.setFont("THSarabun", 16)
	p.drawString(100, 720, f"ชื่อผู้ใช้: {owner.user.first_name} {owner.user.last_name}")
	p.drawString(100, 700, f"ตำแหน่ง: {getattr(owner, 'jobposition_name',)}")
	p.drawString(100, 680, f"หน่วยงาน: {accessory.section }")
	p.drawString(100, 660, f"รหัสครุภัณฑ์: {accessory.deviceID or '-'}")
	p.drawString(100, 640, f"ยี่ห้อ / รุ่น: {accessory.combranding} / {accessory.commodel or '-'}")
	p.drawString(100, 620, f"คุณลักษณะครุภัณฑ์: {accessory.comspec} ")

	# ช่องว่างให้ลงชื่อ
	p.drawString(130, 580, "ข้าพเจ้ามีความประสงค์ขอคืนครุภัณฑ์นี้ซึ่งเป็นทรัพย์สินทางราชการ ซึ่งขอยืมใช้ปฎิบัติงานราชการ ")    
	p.drawString(100, 560, "ตั้งแต่วันที่..........เดือน...................พ.ศ.........")
	p.drawString(100, 540, "ถึงวันที่........เดือน.....................พ.ศ.........เพื่อประโยชน์ทางราชการต่อไป")
	p.drawString(300, 510, "ลงชื่อ.....................................................ผู้ส่งคืนครุภัณฑ์ ")    
	p.drawString(340, 490, f" ({owner.user.first_name} {owner.user.last_name})")
	p.drawString(320, 470, f"  วันที่ส่งคืน.................................... ")

	p.drawString(300, 410, "ลงชื่อ.....................................................ผู้รับคืน ")    
	p.drawString(320, 390, f" (.....................................................)")
	p.drawString(300, 370, f"  วันที่ส่งคืน.......................................... ")

	p.showPage()
	p.save()

	return response

def Register(request):
	if request.method == 'POST':
		register = Register_Form(request.POST or None)
		if register.is_valid():
			user = register.save(commit=False)
			password = register.cleaned_data['password']

			try:
				validate_password(password, user=user)  # ตรวจสอบตามกฎ
			except ValidationError as e:
				for error in e.messages:
					messages.warning(request, error)
				return render(request, "cmsapp_backend/pages-register.html", {'register': register})

			user.set_password(password)
			user.save()
			messages.success(request, "ลงทะเบียนสำเร็จ")
		else:
			messages.warning(request, "กรุณาตรวจสอบข้อมูล")
			return render(request, "cmsapp_backend/pages-register.html", {'register': register})

	context = {'register': Register_Form()}
	return render(request, 'cmsapp_backend/pages-register.html', context)
	

############## Start Module For Administrator ################################################################3#######

@login_required
@never_cache
def ComputerManagement(request):

		Com = ComputerAccessory.objects.annotate(repair_count=Count('repairs')).order_by('-id')[:10]
		for c in Com:
			c.cover = c.hw_photos.first()


		if request.user.profileuser.usergroup :	

				if request.method == 'POST':
					
				# create object of form
					formComp = AddComAccessoryForm(request.POST)
					photo = request.FILES.getlist("comphoto")
					
				# check if form data is valid you can use 2 form conditi here #if formComp1.is_valid() and if formComp2.is_valid():
					if formComp.is_valid():
							
						f = formComp.save(commit=False)
						f.save()
						for img in photo:
							PhotoComputerAccessory.objects.create(hw_number=f,hw_photo=img)
						#messages.success(request,"ถูกต้อง/บันทึกเรียบร้อยแล้ว ")
						messages.success(request,"ถูกต้อง/บันทึกเรียบร้อยแล้ว ")
						return redirect('com_management_page')
						
					else:
						#messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง") no
						messages.warning(request,"โปรดตรวจสอบข้อมูล")
						return render(request, "cmsapp_backend/computermanagement.html",{'formComp': formComp } )

				context = {'formComp': AddComAccessoryForm(),'Com':Com,}

				return render(request, "cmsapp_backend/computermanagement.html", context)

		else:	
			return redirect('home_page')


@login_required()
@never_cache  #ย้ายไปอยู่กับหน้าโปรไฟล์user
def AddRepair(request,repair_id ):

	repairItem = ComputerAccessory.objects.get(id = repair_id)
	#status = RepairStatus.objects.filter(id=2)
	#print(repairItem.id,repairItem.comstatus,repairItem.owner_id,repairItem.deviceID,repairItem.remark)
	
	if 	request.user.profileuser.usergroup:
			if request.method == 'POST':

				formRepair = AddRepairForm(request.POST or None, request.FILES or None)
				updatestatus = AddComStatusToComputerAcc(request.POST or None,request.FILES or None)

				if formRepair.is_valid() and updatestatus.is_valid():
					
					try:
						repair_status = RepairStatus.objects.get(status="กำลังซ่อม")
					except RepairStatus.DoesNotExist:
						repair_status = None 
						messages.error(request,"ไม่พบสถานะ 'กำลังซ่อม' ในฐานข้อมูล")	
					
					if repair_status:

						repairItem.comstatus =  repair_status#  กำลังซ่อม
						repairItem.save()
						#AddComStatusToComputerAcc.save()

						formRepair.instance.owner = request.user.profileuser	
						formRepair.instance.deviceID = repairItem.deviceID						
						formRepair.instance.hw_id = repairItem
						# formRepair.instance.repairstatus = repair_status
						
						formRepair.save()
							
						messages.success(request,"แจ้งซ่อมเรียบร้อยแล้ว")
					else:
						return render(request,"cmsapp_backend/comrepairing.html")


				else:
					#messages.warning(request,"captcha ผิด ลองใหม่อีกครั้ง")
					return render(request,"cmsapp_backend/comrepairing.html")
			
			context = {'formRepair': AddRepairForm(),'repairItem':repairItem,}

			return render(request,'cmsapp_backend/comrepairing.html',context)

	else:
		return redirect('home_page')


@login_required()
@never_cache
def CyberSecurityManagement(request):
	cyber = Cyber_Alert.objects.all()
	if request.user.profileuser.usergroup == 'admin':	

			if request.method == 'POST':
				
			# create object of form
				form = AddCyberAlertForm(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if form.is_valid():
					#form.instance.owner = request.user.profileuser								
					form.save()
					messages.success(request,"ถูกต้อง/บันทึกเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/cybersecurity.html",{'form':form} )

			context = {'form': AddCyberAlertForm(),'cyber':cyber,}

			return render(request,'cmsapp_backend/cybersecurity.html',context)
	else:	
		return redirect('home_page')


@login_required()
@never_cache
def AddCyberPolicy(request):

	policy = ITWebBlog.objects.all()
	if request.user.profileuser.usergroup == 'admin':	

			if request.method == 'POST':
				
			# create object of form
				form = AddCyberPolicyForm(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if form.is_valid():
					form.instance.reporter = request.user.profileuser								
					form.save()
					messages.success(request,"ถูกต้อง/บันทึกเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/cyber-policy.html",{'form':form} )

			context = {'form': AddCyberPolicyForm(),'policy':policy,}

			return render(request,'cmsapp_backend/cyber-policy.html',context)

	else:	
		return redirect('home_page')

@login_required() #ย้ายไปอยู่กับหน้าโปรไฟล์user
@never_cache
def ShowAllUser(request):
	alluser = ProfileUser.objects.all()
	context = {'alluser': alluser,}
	return render(request,'cmsapp_backend/alluser.html',context)


@login_required()
@never_cache
def ShowAllRepair(request):
	showrepair = RepairAndPartChange.objects.all().order_by('-datestart')
	#for i in showrepair:

		#print(i.owner.photo.url) #test for loop
	context = {'showrepair':showrepair}
	return render(request,'cmsapp_backend/showallrepair.html',context)

@login_required()
@never_cache
def RepairReport(request,item_id):
	repairReport = RepairAndPartChange.objects.get(id=item_id)
	
	context = {'repairReport':repairReport}
	return render(request,'cmsapp_backend/repairreport.html',context)
	

@login_required()
@never_cache
def RepairResultSave(request, item_id):
	if not request.user.profileuser.usergroup:
		return redirect('home_page')

	repairitem = get_object_or_404(RepairAndPartChange, id=item_id)
	status = get_object_or_404(ComputerAccessory, id=repairitem.hw_id_id, owner=repairitem.owner_id)

	formRepairItem = AddRepairItemForm(request.POST or None, request.FILES or None, instance=repairitem)
	updatestatus = UpdateComStatus(request.POST or None, request.FILES or None, instance=status)

	if request.method == 'POST':
		if formRepairItem.is_valid() and updatestatus.is_valid():
			formRepairItem.instance.itsupport = request.user.profileuser
			repair_status = RepairStatus.objects.filter(status=repairitem.repairstatus).first()
			if not repair_status:
				messages.error(request, f"ไม่พบสถานะ '{repairitem.repairstatus}' ในฐานข้อมูล")
			else:
				status.comstatus = repair_status				
				status.save()
				formRepairItem.save()
				messages.success(request, "ดำเนินการบันทึกข้อมูลแล้ว")
				return redirect('repairresultsave_page', item_id=item_id)

	context = {
		'formRepairItem': formRepairItem,
		'repairitem': repairitem,
	}
	return render(request, 'cmsapp_backend/repairresult.html', context)


@login_required
@never_cache
def RepairResultUpdate(request, item_id):
	repairitem = get_object_or_404(RepairAndPartChange, id=item_id)
	status = get_object_or_404(ComputerAccessory, id=repairitem.hw_id_id, owner=repairitem.owner_id)

	# จำกัดสิทธิ์
	if request.user.profileuser.usergroup not in ['admin', 'itsupport']:
		return redirect('home_page')

	if request.method == 'POST':
		UpdateRepairItem = UpdateRepairItemForm(request.POST, request.FILES, instance=repairitem)
		updatestatus = UpdateComStatus(request.POST, request.FILES, instance=status)

		if UpdateRepairItem.is_valid() and updatestatus.is_valid():
			# อัปเดตสถานะเครื่อง ตามสถานะการซ่อมที่เลือก
			if repairitem.repairstatus:
				status.comstatus = repairitem.repairstatus
				status.save()

			UpdateRepairItem.save()
			updatestatus.save()

			messages.success(request, "บันทึกข้อมูลการซ่อมเรียบร้อยแล้ว")
			# return render(request, 'cmsapp_backend/repairresultupdate.html')
			return redirect('repairresultupdate_page', item_id=item_id)
		else:
			messages.error(request, "ฟอร์มไม่ถูกต้อง: " + str(UpdateRepairItem.errors) + str(updatestatus.errors))

	else:
		UpdateRepairItem = UpdateRepairItemForm(instance=repairitem)
		updatestatus = UpdateComStatus(instance=status)

	context = {
		'UpdateRepairItem': UpdateRepairItem,
		'updatestatus': updatestatus,
		'repairitem': repairitem,
	}
	return render(request, 'cmsapp_backend/repairresultupdate.html', context)



from django.http import JsonResponse
from sparepart.models import PartsSubCatName



def load_subcategories_bkend(request):
	category_id = request.GET.get('category_id')  # ต้องตรงกับ JS ที่ส่งมา
	subcategories = []

	if category_id:
		subcategories = PartsSubCatName.objects.filter(
			parts_cat_name_id=category_id
		).values('id', 'parts_sub_name')  # ใช้ฟิลด์ parts_sub_name ตามที่มีจริงใน model

	return JsonResponse(list(subcategories), safe=False)


@login_required()
@never_cache
def BorrowDeviceSave(request):
	borrowAll = BorrowDevice.objects.all()
	
	if request.user.profileuser.usergroup == 'editer' or 'reporter' or 'admin':
	
			if request.method == 'POST':
				#edit and update item
				BorrowItem = AddBorrowForm(request.POST or None, request.FILES or None) #AddBorrowForm

				if BorrowItem.is_valid():
					BorrowItem.instance.user_borrow = request.user.profileuser					
					
					BorrowItem.save()
					messages.success(request,"ดำเนินการแล้ว")
				else:
					# messages.warning(request,"captcha ผิด ลองใหม่อีกครั้ง")
					return render(request,"cmsapp_backend/borrowdevice.html")

		
			context = {'BorrowItem': AddBorrowForm(),'borrowAll':borrowAll,}

			return render(request,'cmsapp_backend/borrowdevice.html',context)

	else:
		return redirect('home_page')
	#print(i.owner.photo.url) #test for loop
	context = {'borrowAll':borrowAll}
	return render(request,'cmsapp_backend/borrowdevice.html',context)

@login_required()
@never_cache
def ShowAllBorrow(request):
	user = request.user.profileuser
	usergroup = request.user.profileuser.usergroup
	print("Usergroup:", usergroup)  # Debugging line
	print("UserID:", user.id)  # Debugging line

	
	# Check if the user group is 'admin'
	if usergroup in ['reporter', 'editer']:
		showborrow = BorrowDevice.objects.filter(user_borrow_id=user.id)
	
		context = {'showborrow': showborrow}
		return render(request, 'cmsapp_backend/showallborrow.html', context)

	elif usergroup == 'admin':
		showborrow = BorrowDevice.objects.all()
		context = {'showborrow': showborrow}
		return render(request, 'cmsapp_backend/showallborrow.html', context)
	else:	
		return redirect('itadmin_page')


	

@login_required()
@never_cache
def BorrowEdit(request,item_id):
	borrowitem = BorrowDevice.objects.get(id=item_id)

	if 	request.user.profileuser.usergroup == 'trainee' or 'admin' :
			if request.method == 'POST':
				#edit and update item
				EditBorrowItem = EditBorrowDeviceItemForm(request.POST or None, request.FILES or None,instance=borrowitem) #EditBorrowDeviceItemForm

				if EditBorrowItem.is_valid():
					EditBorrowItem.instance.admin_allowborrow = request.user.profileuser					

					
					EditBorrowItem.save()
					messages.success(request,"บันทึกการยืมแล้ว")
				else:
					messages.warning(request,"captcha ผิด ลองใหม่อีกครั้ง")
					return render(request,"cmsapp_backend/editborrow.html")

		
			context = {'EditBorrowItem': EditBorrowDeviceItemForm(),'borrowitem':borrowitem,}

			return render(request,'cmsapp_backend/editborrow.html',context)

	else:
		return redirect('home_page')
	#print(i.owner.photo.url) #test for loop
	context = {'borrowitem':borrowitem}
	return render(request,'cmsapp_backend/editborrow.html',context)

@login_required()
@never_cache
def EditBorrowReturn(request,item_id): 
	borrowitem = BorrowDevice.objects.get(id=item_id)
	
	if 	request.user.profileuser.usergroup == 'trainee' or 'admin':
			if request.method == 'POST':
				#edit and update item
				EditBorrowReturnItem = EditBorrowReturnForm(request.POST or None, request.FILES or None,instance=borrowitem) #EditBorrowDeviceItemForm

				if EditBorrowReturnItem.is_valid():
					EditBorrowReturnItem.instance.admin_returnback = request.user.profileuser					

					
					EditBorrowReturnItem.save()
					messages.success(request,"บันทึกการคืนแล้ว") 
				else:
					# messages.warning(request,"captcha ผิด ลองใหม่อีกครั้ง")
					return render(request,"cmsapp_backend/borrowreturn.html")

		
			context = {'EditBorrowReturnItem': EditBorrowReturnForm(),'borrowitem':borrowitem,}

			return render(request,'cmsapp_backend/borrowreturn.html',context)

	else:
		return redirect('home_page')
	#print(i.owner.photo.url) #test for loop
	context = {'borrowitem':borrowitem}
	return render(request,'cmsapp_backend/editborrow.html',context)

@login_required()
@never_cache
def BorrowReport(request,item_id):
	borrowReport = BorrowDevice.objects.get(id=item_id)

	context = {'borrowReport':borrowReport}
	return render(request,'cmsapp_backend/borrowreport.html',context)


@login_required()
@never_cache
def ShowComReq(request):
			Comreq = ComRequest.objects.all()
		
			if request.method == 'POST':
				
			# create object of form
				form = AddComReqForm(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if form.is_valid():
					
					jobdis = form.cleaned_data['jobdis']					
					form.instance.user = request.user.profileuser
					
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/ลงข่าวเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/showcomreq.html",{'form':form} )

			context = {'form': AddComReqForm(),'Comreq':Comreq,}

			return render(request, "cmsapp_backend/showcomreq.html", context)


@login_required() #ย้ายไปอยู่กับหน้าโปรไฟล์user
@never_cache
def DeviceProfile(request):

	request.user.is_authenticated
	User = request.user.profileuser

	#User = request.user.profileuser.id # ฟังก์ชั่น รับค่า user เพื่อ query ค่าของ user นั้นๆ ในตาราง ComputerAccessory		
	CA = ComputerAccessory.objects.filter( owner =  User )

	CSR = RepairAndPartChange.objects.select_related('owner').filter(repairstatus_id=1,owner=User)
	SR = RepairAndPartChange.objects.filter(repairstatus_id=1,owner_id=User)

	# print(SR)

	context = {'CA':CA,'CSR':CSR}
	for i in CA: 
		print(i.id)
		print(i.owner)
		print(i.comstatus)

	return render(request,'cmsapp_backend/device-profile.html',context)

@login_required() #ย้ายไปอยู่กับหน้าโปรไฟล์user
@never_cache
def UserProfile(request):
	if not hasattr(request.user, 'profileuser'):
		return somethingwrong_alert(
			message="ไม่พบข้อมูลโปรไฟล์ผู้ใช้",
			title="โปรไฟล์ไม่สมบูรณ์ กรุณาติดต่อผู้ดูแลระบบ",
			icon="warning",
			redirect_url_name="itadmin_page"
		)

	profile = request.user.profileuser

	if profile.usergroup not in ['admin','superuser','editor','reporter','trainee']:
		return somethingwrong_alert(
			message="คุณไม่มีสิทธิ์เข้าถึงหน้านี้",
			title="สิทธิ์ไม่เพียงพอ กรุณาติดต่อผู้ดูแลระบบ",
			icon="error",
			redirect_url_name="itadmin_page"
		)

	return render(request, 'cmsapp_backend/user-profile.html')

	

# Start update user frontend side
@login_required()
@never_cache
def UpdateProfile(request,userprofile_id):
	UserProfile = request.user.profileuser
	updateUser = UpdateUserProfileForm(instance=UserProfile)
	print(UserProfile);

	if request.method == "POST":
		updateUser = UpdateUserProfileForm(request.POST,request.FILES,instance=UserProfile)
		if updateUser.is_valid():
			updateUser.save()
			messages.success(request,'แก้ไขโปรไฟล์สำเร็จแล้ว')
		else:
			return redirect('userprofile_page')

	context = {'updateUser':updateUser,}
	return render(request,'cmsapp_backend/update-user-profile.html',context)	

# Start update user backend side

@login_required()
@never_cache
def UpdateProfileUserAdmin(request,user_id):
	#UserProfile = request.user.profileuser
	edituser = ProfileUser.objects.get(user_id=user_id)	
	UpdateUser = UpdateProfileUserAdminForm(instance=edituser)
	print(edituser.user.id,edituser.user.username,edituser.user.first_name);

	if request.method == "POST":
		UpdateUser = UpdateProfileUserAdminForm(request.POST,request.FILES,instance=edituser)
		if UpdateUser.is_valid():
			UpdateUser.save()
			messages.success(request,'แก้ไขโปรไฟล์สำเร็จแล้ว')
		else:
			return redirect('userprofile_page')

	context = {'UpdateUser':UpdateUser,'edituser':edituser,}
	return render(request,'cmsapp_backend/update-user-adminpage.html',context)

	
############## End Module For Administrator ########################################################################

############## Start Module For Site Setting ########################################################################


@login_required()
@never_cache
def HeaderSetting(request):
	if request.user.profileuser.usergroup == 'admin' or 'editor':
		
			if request.method == 'POST':			
			# create object of form
			
				formH = AddPhotoHeadHomePageForm(request.POST or None, request.FILES or None)

				
			# check if form data is valid
				if formH.is_valid():
					title = formH.cleaned_data['title']
					post = formH.cleaned_data['post']
					#cleaned_da = form.cleaned_data
					# save the form data to model
					formH.save()
					messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
				else:
					messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/headersetting.html",{'formH':formH} )
			context = {	'formH': AddPhotoHeadHomePageForm(),}			
			return render(request, "cmsapp_backend/headersetting.html", context)
	else:	
		return redirect('home_page')			


@login_required()
@never_cache
def FooterSetting(request):
	if request.user.profileuser.usergroup == 'admin' or 'editor':
	
			if request.method == 'POST':			
			# create object of form
			
				form = AddDocterForm(request.POST or None, request.FILES or None)
				
			# check if form data is valid
				if form.is_valid():
					name = form.cleaned_data['name']
					lastname = form.cleaned_data['lastname']
					msg = form.cleaned_data['msg']
					scholarposition = form.cleaned_data['scholarposition']

					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
				else:
					messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/footersetting.html",{'form':form} )
			context = {	'form': AddDocterForm(),}			
			return render(request, "cmsapp_backend/footersetting.html", context)
	else:	
		return redirect('home_page')			


@login_required()
@never_cache
def FontAweasome(request):
	if request.user.profileuser.usergroup == 'editor' or 'admin' :
		

				if request.method == 'POST':			
				# create object of form
				
					form = AddFontAweasomeForm(request.POST or None, request.FILES or None)

					
				# check if form data is valid
					if form.is_valid():
						fontname = form.cleaned_data['fontname']
										
						#cleaned_da = form.cleaned_data
						# save the form data to model
						form.save()
						messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
					else:
						messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
						return render(request, "cmsapp_backend/fontaweasome.html",{'form':form} )
				context = {	'form': AddFontAweasomeForm(),}			
				return render(request, "cmsapp_backend/fontaweasome.html", context)	


	else: 	
		return redirect('home_page')



@login_required()
@never_cache
def NewsCategorybk(request):

	newscat = NewsCategory.objects.all().order_by('id')
	context = {'newscats':newscat}

	if request.user.profileuser.usergroup == 'admin' or 'editor':

			if request.method == 'POST':			
			# create object of form
			
				form = AddNewCategoryForm(request.POST or None, request.FILES or None)

				
			# check if form data is valid
				if form.is_valid():
					categ = form.cleaned_data['categ']
									
					#cleaned_da = form.cleaned_data	
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
				else:
					messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/newscategory.html",{'form':form} )
			context = {	'form': AddNewCategoryForm(),
						'newscat':newscat }			
			return render(request, "cmsapp_backend/newscategory.html", context)
	else:	
		return redirect('home_page')		
	

@login_required()
@never_cache
def Sectionbk(request):
	if request.user.profileuser.usergroup == 'admin' or 'editor':
			if request.method == 'POST':			
			# create object of form
			
				form = AddSectionForm(request.POST or None, request.FILES or None)

				
			# check if form data is valid
				if form.is_valid():
					sectionsname = form.cleaned_data['sectionsname']
					tel = form.cleaned_data['tel']
									
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
				else:
					messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/section.html",{'form':form} )
			context = {	'form': AddSectionForm(),}			
			return render(request, "cmsapp_backend/section.html", context)
	else:	
		return redirect('home_page')


@login_required()
@never_cache
def AdsBanner(request):
	if request.user.profileuser.usergroup == 'admin' or 'editor':

			if request.method == 'POST':			
			# create object of form
			
				form = AddIconAdsForm(request.POST or None, request.FILES or None)

				
			# check if form data is valid
				if form.is_valid():
					
					link = form.cleaned_data['link']
									
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
				else:
					messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/adsbanner.html",{'form':form} )
			context = {	'form': AddIconAdsForm(),}			
			return render(request, "cmsapp_backend/adsbanner.html", context)
	else:	
		return redirect('home_page')	
	
@login_required()
@never_cache
def ExternalLink(request):
	if request.user.profileuser.usergroup == 'editor' or 'admin':

			if request.method == 'POST':			
			# create object of form
			
				form = AddLinkExternalForm(request.POST or None, request.FILES or None)
				
			# check if form data is valid
				if form.is_valid():
					
					text = form.cleaned_data['text']
					url = form.cleaned_data['url']
									
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
				else:
					messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/external_link.html",{'form':form} )
			context = {	'form': AddLinkExternalForm(),}			
			return render(request, "cmsapp_backend/external_link.html", context)
	else:	
		return redirect('home_page')	





############## End Module For Site Setting ########################################################################



############## End Module For Site Reprtor ########################################################################

@login_required()
@never_cache
def Onepagebk(request):
	if request.user.profileuser.usergroup == 'reporter' or 'admin':

			if request.method == 'POST':			
			# create object of form
			
				form = AddOnePageForm(request.POST or None, request.FILES or None)
				
				# check if form data is valid
				if form.is_valid():
					
					title = form.cleaned_data['title']
					form.instance.user = request.user.profileuser				
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/เพิ่มเรียบร้อยแล้ว ")				
				else:
					messages.warning(request,"พิมพ์อักษรไม่ถูกต้อง/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/onepagebk_page.html",{'form':form} )
			context = {	'form': AddOnePageForm(),}			
			return render(request, "cmsapp_backend/onepagebk_page.html", context)
	else:	
		return redirect('home_page')

@login_required()
@never_cache
def AddNewsForm(request):

	lastnews = News.objects.all().order_by('id').reverse()[:2]
	if request.user.profileuser.usergroup == 'reporter' or 'admin':

			if request.method == 'POST':
				
			# create object of form
				form = NewsForm(request.POST or None, request.FILES or None)
				photo = request.FILES.getlist("photo1")			
			# check if form data is valid
				if form.is_valid():
					
					title = form.cleaned_data['title']
					post = form.cleaned_data['post']
					form.instance.reporter = request.user.profileuser  #add user input auto  ot model  news when login
					f = form.save(commit=False)
					f.save()
					for img in photo:
						NewsPhoto.objects.create(news_id=f,news_photo=img)

					
					messages.success(request,"ถูกต้อง/ลงข่าวเรียบร้อยแล้ว ")
					#return HttpResponseRedirect('addnewsform.html')
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/addnewsform.html",{'form':form} )

			context = {	'form':NewsForm(),'lastnews':lastnews,}			
			return render(request, "cmsapp_backend/addnewsform.html", context)
	else:	
		return redirect('home_page')	

@login_required()
@never_cache
def AddArtical(request):

	if request.user.profileuser.usergroup == 'reporter' or 'admim':

			if request.method == 'POST':
				
			# create object of form
				form = AddArtical_Form(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if form.is_valid():
					

					title = form.cleaned_data['title']
					post = form.cleaned_data['post']
					form.instance.reporter = request.user.profileuser
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/ลงข่าวเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/addhealtharticalform.html",{'form':form} )

			context = {	'form': AddArtical_Form(),}			
			return render(request, "cmsapp_backend/addhealtharticalform.html", context)

	else:	
		return redirect('home_page')

@login_required()
@never_cache
def AddConference(request):

	if request.user.profileuser.usergroup == 'editor' or 'admin':

			if request.method == 'POST':
				
			# create object of form
				form = AddConferenceForm(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if form.is_valid():
					
					title = form.cleaned_data['title']
					schedule = form.cleaned_data['schedule']
					form.instance.user = request.user.profileuser
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/ลงข่าวเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/addconferenceform.html",{'form':form} )

			context = {	'form': AddConferenceForm(),}
			return render(request, "cmsapp_backend/addconferenceform.html", context)

	else:
		return HttpResponse("คุณไม่มีสิทธิ์เข้าถึง กรุณาติดต่อผู้ดูแลระบบ")
		return redirect('home_page')

@login_required
@never_cache
def AddOurService(request):

	if request.user.profileuser.usergroup == 'editor' or 'admin':

			if request.method == 'POST':
				
			# create object of form
				form = AddOurServiceForm(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if form.is_valid():
					
					title = form.cleaned_data['title']
					msg = form.cleaned_data['msg']
					
					#schedule = form.cleaned_data['schedule']
					#form.instance.user = request.user.profileuser
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/เพิ่มบริการเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/addourservicesform.html",{'form':form} )

			context = {	'form': AddOurServiceForm(),}
			return render(request, "cmsapp_backend/addourservicesform.html", context)

	else:
		return HttpResponse("คุณไม่มีสิทธิ์เข้าถึง กรุณาติดต่อผู้ดูแลระบบ")
		return redirect('home_page')

@login_required
@never_cache
def AddFileDownload(request):

	if request.user.profileuser.usergroup == 'editor' or 'admin':
	
			if request.method == 'POST':
				
			# create object of form
				form = AddFileDownloadForm(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if form.is_valid():
					
					title = form.cleaned_data['title']
					file = form.cleaned_data['file']
					form.instance.user = request.user.profileuser
					#cleaned_da = form.cleaned_data
					# save the form data to model
					form.save()
					messages.success(request,"ถูกต้อง/ลงข่าวเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/addfiledownloadform.html",{'form':form} )

			context = {'form': AddFileDownloadForm(),}
			return render(request, "cmsapp_backend/addfiledownloadform.html", context)
	else:	
		return redirect('home_page')

############## End Module For Site Reprtor ########################################################################

#####################AddWorkReport####################

@login_required
@never_cache
def AddWorkReport(request):
	# เช็คว่ามี profile หรือไม่
	if not hasattr(request.user, 'profileuser'):
		return somethingwrong_alert(
			message="ไม่พบโปรไฟล์ผู้ใช้ กรุณาลงทะเบียนก่อน",
			title="โปรไฟล์ไม่สมบูรณ์ กรุณาติดต่อผู้ดูแลระบบ",
			icon="warning",
			redirect_url_name="itadmin_page"
		)

	profile = request.user.profileuser

	if profile.usergroup not in ['trainee', 'admin']:
		return somethingwrong_alert(
			message="คุณไม่มีสิทธิ์เข้าถึงหน้านี้",
			title="สิทธิ์ไม่เพียงพอ กรุณาติดต่อผู้ดูแลระบบ",
			icon="error",
			redirect_url_name="itadmin_page"
		)

	trainee = profile
	workview = DailyWorkReport.objects.filter(usertrinee_id=trainee.id)

	if request.method == 'POST':
		forminsert = AddWorkReportForm(request.POST)
		photos = request.FILES.getlist("images")

		if forminsert.is_valid():
			forminsert.instance.usertrinee = trainee
			report = forminsert.save()

			for img in photos:
				ImagesCloud.objects.create(workid=report, images=img)

			messages.success(request, "บันทึกรายงานเรียบร้อยแล้ว")
		else:
			messages.warning(request, "พิมพ์อักษรผิด หรือข้อมูลไม่ครบ")
			return render(request, "cmsapp_backend/addworkreport.html", {
				'forminsert': forminsert,
				'workview': workview
			})

	context = {
		'forminsert': AddWorkReportForm(),
		'workview': workview
	}
	return render(request, "cmsapp_backend/addworkreport.html", context)

#####################EndAddWorkReport####################
#####################StartAllWorkReportView####################

@login_required()
@never_cache
def AllWorkReportView(request):

		# เช็คว่ามี profile หรือไม่
	if not hasattr(request.user, 'profileuser'):
		return somethingwrong_alert(
			message="ไม่พบโปรไฟล์ผู้ใช้ กรุณาลงทะเบียนก่อน",
			title="โปรไฟล์ไม่สมบูรณ์ กรุณาติดต่อผู้ดูแลระบบ",
			icon="warning",
			redirect_url_name="itadmin_page"
		)

	profile = request.user.profileuser
	if profile.usergroup not in ['trainee', 'admin']:
		return somethingwrong_alert(
			message="คุณไม่มีสิทธิ์เข้าถึงหน้านี้",
			title="สิทธิ์ไม่เพียงพอ กรุณาติดต่อผู้ดูแลระบบ",
			icon="warning",
			redirect_url_name="itadmin_page"
		)

	user = profile
	workview = DailyWorkReport.objects.filter(usertrinee_id=user.id)
	totalworkshop = DailyWorkReport.objects.filter(usertrinee_id=user.id).aggregate(total=Count('id'))['total']
	workimage = ImagesCloud.objects.all()
	print('totalworkshop::>',totalworkshop)
	context = {
				'workview':workview,
				# 'workview_trn':workview_trn,
				'workimage':workimage,
				'totalworkshop':totalworkshop,
				}	
	return render(request, "cmsapp_backend/allworkreport.html", context)


#####################EndAllWorkReportView####################
	
	
#####################StarWorkViewDetails####################

@login_required
@never_cache
def WorkReportDetail(request,work_id):

	workview = get_object_or_404(DailyWorkReport,id=work_id)	
	workimage = ImagesCloud.objects.filter(workid=work_id)

	context = {
				'workview':workview,
				'workimage':workimage

				}
		
	return render(request, "cmsapp_backend/workreportdetail.html", context)
	

#####################EndWorkViewDetails####################

@login_required
@never_cache
def Update_success(request):
	return render(request,"cmsapp_backend/update-success-page.html")


####################### start function traineee##########################
@login_required
@never_cache
def RatingWorkingTrainee(request, work_id):
	# ตรวจสอบว่า user มี ProfileUser และ usergroup
	if not hasattr(request.user, 'profileuser') or request.user.profileuser.usergroup != 'admin':
		return redirect('itadmin_page')  # หรือแสดง error page

	report = get_object_or_404(DailyWorkReport, id=work_id)

	if request.method == 'POST':
		Ratingform = WorkRatingForm(request.POST, instance=report)
		if Ratingform.is_valid():
			updated_report = Ratingform.save(commit=False)
			updated_report.admin_control = request.user.profileuser
			updated_report.save()
			return redirect('workratingtrainee_page', work_id=report.id)
	else:
		Ratingform = WorkRatingForm(instance=report)

	return render(request, "cmsapp_backend/workrating.html", {
		'Ratingform': Ratingform,
		'report': report,
	})

@login_required
@never_cache
def ShowAllReportView(request):
	
	if request.user.profileuser.usergroup == 'admin':
		user = request.user.profileuser
		ReportView = DailyWorkReport.objects.all()
		context = {'ReportView':ReportView}
		return render(request, "cmsapp_backend/showallreportview.html", context)
	return redirect('itadmin_page')


@login_required
@never_cache
def AddTrainee(request):
	
	if not hasattr(request.user, 'profileuser'):
		return somethingwrong_alert(
			message="ไม่พบข้อมูลโปรไฟล์ผู้ใช้",
			title="โปรไฟล์ไม่สมบูรณ์ กรุณาติดต่อผู้ดูแลระบบ",
			icon="warning",
			redirect_url_name="itadmin_page"
		)

	profile = request.user.profileuser
	if profile.usergroup not in ['trainee', 'admin']:
		return somethingwrong_alert(
			message="คุณไม่มีสิทธิ์เข้าถึงหน้านี้",
			title="สิทธิ์ไม่เพียงพอ กรุณาติดต่อผู้ดูแลระบบ",
			icon="error",
			redirect_url_name="itadmin_page"
		)  

	if request.method == 'POST':
		formtrainee = AddTraineeForm(request.POST, request.FILES)
		if formtrainee.is_valid():
			formtrainee.instance.traineeUser_id = profile
			formtrainee.save()
			messages.success(request, "บันทึกรายชื่อนักศึกษาแล้ว")
			return redirect('showtrainee_page')  # หรือหน้าอื่นหลังบันทึกสำเร็จ
		else:
			messages.warning(request, "พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
			return render(request, "cmsapp_backend/addtraineeform.html", {'formtrainee': formtrainee})

	# GET request
	context = {'formtrainee': AddTraineeForm()}
	return render(request, "cmsapp_backend/addtraineeform.html", context)


@login_required
@never_cache
def ShowTrainee(request):
	if not hasattr(request.user, 'profileuser'):
		return somethingwrong_alert(
			message="ไม่พบข้อมูลโปรไฟล์ผู้ใช้",
			title="โปรไฟล์ไม่สมบูรณ์ กรุณาติดต่อผู้ดูแลระบบ",
			icon="warning",
			redirect_url_name="itadmin_page"
		)

	profile = request.user.profileuser

	if profile.usergroup == 'trainee':
		# นักศึกษาแสดงเฉพาะตัวเอง
		try:
			trainee = Trainee.objects.get(traineeUser_id=profile)
		except Trainee.DoesNotExist:
			return somethingwrong_alert(
				message="ไม่พบข้อมูลผู้ฝึกงานในระบบ",
				title="เกิดข้อผิดพลาด",
				icon="error",
				redirect_url_name="itadmin_page"
			)
		context = {'trainee': [trainee]}  # แปลงเป็น list เพื่อ uniform
	elif profile.usergroup == 'admin':
		# admin แสดงทั้งหมด
		trainee = Trainee.objects.all()
		context = {'trainee': trainee}

	return render(request, "cmsapp_backend/showtrainee.html", context)



@login_required
@never_cache
def ShowAllTrainee(request):
	
	if request.user.profileuser.usergroup == 'admin' or request.user.profileuser.usergroup == 'trainee' :
		user = request.user.profileuser
		trainee = Trainee.objects.all()
		context = {'trainee':trainee}
		return render(request, "cmsapp_backend/showalltrainee.html", context)
	return redirect('registrainee_page')



@login_required
@never_cache
def TraineeDetails(request,trainee_id):
	trainee = Trainee.objects.filter(id=trainee_id)
	context = {'trainee':trainee}
	return render(request, "cmsapp_backend/traineedetails.html", context)
	
####################### end function traineee############################

@login_required
@never_cache
def AddOfficeCenter(request):
	program = ProgramOffice.objects.all()

	if request.user.profileuser.usergroup == 'editor' or 'admin':
	
			if request.method == 'POST':
				
			# create object of form
				formprogram = AddProgramOfficeForm(request.POST or None, request.FILES or None)
			
			# check if form data is valid
				if formprogram.is_valid():

					formprogram.save()
					messages.success(request,"ถูกต้อง/ลงข่าวเรียบร้อยแล้ว ")
					
				else:
					messages.warning(request,"พิมพ์อักษรผิด/ลองใหม่อีกครั้ง")
					return render(request, "cmsapp_backend/addofficecenterform.html",{'formprogramoffice':formprogramoffice} )

			context = {'formprogram': AddProgramOfficeForm(),}
			return render(request, "cmsapp_backend/addofficecenterform.html", context)
	else:	
		return redirect('home_page')

	
	context = {'program':program}
	return render(request,'cmsapp_backend/addofficecenterform.html',context)

@login_required
@never_cache
def ItAdmin(request):
	sec = Sections.objects.all().order_by('id')

	
	gcount = ProfileUser.objects.aggregate(
		digi = Count("id",filter=Q(sections_id=1)),
		hpmt = Count("id",filter=Q(sections_id=2)),
		ctpt = Count("id",filter=Q(sections_id=3)),
		tmd = Count("id",filter=Q(sections_id=4)),
		hr = Count("id",filter=Q(sections_id=5)),
		law = Count("id",filter=Q(sections_id=6)),
		plan = Count("id",filter=Q(sections_id=7)),
		dev = Count("id",filter=Q(sections_id=8)),
		ncd = Count("id",filter=Q(sections_id=9)),
		cd = Count("id",filter=Q(sections_id=10)),
		env = Count("id",filter=Q(sections_id=12)),
		ins = Count("id",filter=Q(sections_id=13)),
		man = Count("id",filter=Q(sections_id=14)),
		bsh = Count("id",filter=Q(sections_id=15)),
		den = Count("id",filter=Q(sections_id=16)),
		)	
	

	
	context = {'sec':sec,'gcount':gcount}
	return render(request,'cmsapp_backend/itadmin_page.html',context)

	
@login_required
@never_cache	
def Homeconf(request):

	return render(request, 'cmsapp_vdoconf/homeconf.html',)


@login_required
@never_cache	
def HomeServer(request):

	return render(request, 'cmsapp_servermainten/homeserver.html',)


	






	
