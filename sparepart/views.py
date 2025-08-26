
from django.shortcuts import render, get_object_or_404,HttpResponse,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from cmsapp.models import * #นำโมเดล model จาก cmsapp มาใช้งาน
import qrcode
from reportlab.lib.utils import ImageReader
from .forms import * 
from django.db.models import Sum,Count,Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,FormView
from django.urls import reverse
from cmsapp_backend.models import * #นำโมเดล model จาก cmsapp_backend มาใช้งาน
from server_mainten.models import * #นำโมเดล model จาก cmsapp_backend มาใช้งาน
from sparepart.models import *
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.units import cm
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
import os
from xhtml2pdf import pisa
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from django.utils import timezone  # gen repair id
from django.db.models import Max # gen repair id 20-8-68

from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
# Register Thai font
font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'THSarabunNew.ttf')
pdfmetrics.registerFont(TTFont('THSarabunNew', font_path))



def MainSpareParts(request):
    stock = PartsStock.objects.all()
    usage_summary = ItemsRepairOrderParts.objects.values('part_id').annotate(
        total_used=Sum('part_amount_use'))
    usage_dict = {item['part_id']: item['total_used'] for item in usage_summary}
    context = {'stock':stock,'usage_dict': usage_dict}

    return render(request, 'sparepart/mainspareparts.html',context )
    # return  HttpResponse(" มีการเชื่อมต่อแล้ว")   


@login_required 
def AddStockParts(request):
    if request.user.profileuser.usergroup in ['admin', 'trainee']:  # Check if user has appropriate permissions
        stock = PartsStock.objects.all()

        if request.method == 'POST':
            # Create an object of form AddStockPartsForm with the POST data
            addstockpart = AddStockPartsForm(request.POST)

            if addstockpart.is_valid():
                # Get the parts_name and amount from the form's cleaned data
                parts_cat_name = addstockpart.cleaned_data['parts_cat_name']
                parts_sub_name = addstockpart.cleaned_data['parts_sub_name']
                parts_details = addstockpart.cleaned_data['parts_details']
                price = addstockpart.cleaned_data['price']
                amount_to_add = addstockpart.cleaned_data['amount']

                # Try to find the existing PartsStock for the given parts_name
                partsstock, created = PartsStock.objects.get_or_create(
                    parts_cat_name=parts_cat_name,
                    parts_sub_name=parts_sub_name,
                    parts_details=parts_details,

                    defaults={'amount': 0,'price':price}  # If a new PartsStock is created, start with 0 amount
                )

                # Update the amount, whether it's a new or existing PartsStock
                partsstock.amount += amount_to_add
                partsstock.save()  # Save the updated stock

                # Provide feedback to the user about the success of the operation
                messages.success(request, "Stock part added successfully!")

                # Optionally, redirect to another page after success
                return redirect('addstockparts_page')  # Redirect to some other view after success

            else:
                # Return the form with validation errors if it's not valid
                return render(request, "sparepart/addstockparts.html", {'addstockpart': addstockpart})

        # For GET request, initialize a fresh form and render the template with stock data
        context = {'addstockpart': AddStockPartsForm(), 'stock': stock}
        return render(request, "sparepart/addstockparts.html", context)

    else:  
        # Redirect to login if user doesn't have permission
        return redirect('login_page')

def Load_Subcategories(request):
    category_id = request.GET.get('parts_cat_name')  
    subcategories = PartsSubCatName.objects.filter(parts_cat_name_id=category_id).values('id', 'parts_sub_name')
    return JsonResponse(list(subcategories), safe=False)


# คำนวนการให้เลขรหัส repair id
def generate_repair_id(): 
    date_part = timezone.now().strftime('%Y%m%d')
    prefix = f"RID{date_part}"

    last = ItemsRepairOrderParts.objects.filter(
        repair_id__startswith=prefix
    ).aggregate(
        max_id=Max("repair_id")
    )["max_id"]

    if last:
        # ตัดเอาเลขท้ายมาบวกต่อ
        last_num = int(last[-3:])
        new_num = last_num + 1
    else:
        new_num = 1

    return f"{prefix}{str(new_num).zfill(3)}"

'''
def generate_repair_id():
    date_part = timezone.now().strftime('%Y%m%d')
    last = ItemsRepairOrderParts.objects.filter(repair_id__startswith=f"R{date_part}").count() + 1
    return f"RID-{date_part}{str(last).zfill(3)}"       
'''



@login_required
def Take_A_Parts(request):
    # ตรวจสอบสิทธิ์ก่อน
    if request.user.profileuser.usergroup not in ['admin',]:
        return redirect('itadmin_page')  # หรือแสดงข้อความ error/403

    # ดึงข้อมูลสต็อกและสรุปการใช้งาน
    parts_stock = PartsStock.objects.all()
    usage_summary = ItemsRepairOrderParts.objects.values('part_id').annotate(
        total_used=Sum('part_amount_use'))
    usage_dict = {item['part_id']: item['total_used'] for item in usage_summary}

    if request.method == 'POST':
        form = AddTake_A_PartsForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_order = request.user.profileuser
            instance.admin_recorder = request.user.profileuser
            instance.save()

            # อัปเดตสต็อก
            instance.part_id.amount -= instance.part_amount_use
            instance.part_id.save()
            
            return redirect('take_a_parts_page')
        else:
            return render(request, "sparepart/take_a_parts.html", {
                'AddTake': form,
                'sp': parts_stock,
                'usage_dict': usage_dict
            })

    # GET request
    repair_id = generate_repair_id()
    form = AddTake_A_PartsForm(initial={'repair_id': repair_id})
    context = {
        'AddTake': form,
        'sp': parts_stock,
        'usage_dict': usage_dict
    }
    return render(request, "sparepart/take_a_parts.html", context)


# https://chatgpt.com/share/67f9db83-4b38-8011-a699-a9509b91e38b
@login_required 
def AddPartsCat(request):
    if request.user.profileuser.usergroup in ['admin' , 'trainee']: 

        if request.method == 'POST':
                    
                # create object of form SerVerMaintenForm
            addpartscat = AddPartsCatForm(request.POST)

            if addpartscat.is_valid():
                
                addpartscat.save()
                return redirect('addpartstype_page')
    
            else:

                return render(request, "sparepart/addpartstype.html",{'addpartscat': addpartscat } )
                    
        context = {'addpartscat': AddPartsCatForm(),}

        return render(request, "sparepart/addpartstype.html", context)

    else:   
        return redirect('login_page')

@login_required 
def AddPartSub(request):
    
    if request.user.profileuser.usergroup in ['admin' , 'trainee']:     
        if request.method == 'POST':                    
            addpartssub = AddPartsSubForm(request.POST)
            if addpartssub.is_valid():
                addpartssub.save()
                return redirect('addpartsub_page')
            else:
                return render(request, "sparepart/addpartsub.html",{'addpartssub': addpartssub } )                  
        context = {'addpartssub': AddPartsSubForm(),}
        return render(request, "sparepart/addpartsub.html", context)

    else:   
        return redirect('login_page')

@login_required 
def AllTake_A_Parts(request):
    sp = ItemsRepairOrderParts.objects.all()
    for i in sp:
        print(i.id,i.computer_id_id)
    context = {'sp':sp}

    return render(request, 'sparepart/alltake_a_parts.html',context )

    # return  HttpResponse(" มีการเชื่อมต่อแล้ว")   


@login_required 
def Generate_repair_pdf(request, pk):
    try:
        item = ItemsRepairOrderParts.objects.get(pk=pk)
        user_order = item.user_order
        admin_recorder = item.admin_recorder
        # ดึงข้อมูลจาก PartRepairImage
        images = PartRepairImage.objects.filter(itemrepair_id=item)
    except ItemsRepairOrderParts.DoesNotExist:
        return HttpResponse("ไม่พบรายการซ่อม", status=404)

    # ===== Register THSarabun Fonts =====
    font_dir = os.path.join(settings.BASE_DIR, 'sparepart', 'fonts')
    font_path = os.path.join(font_dir, 'THSarabun.ttf')
    bold_font_path = os.path.join(font_dir, 'THSarabun Bold.ttf')

    if not os.path.exists(font_path) or not os.path.exists(bold_font_path):
        return HttpResponse("ไม่พบไฟล์ฟอนต์ THSarabun", status=500)

    pdfmetrics.registerFont(TTFont('THSarabun', font_path))
    pdfmetrics.registerFont(TTFont('THSarabun-Bold', bold_font_path))
    registerFontFamily('THSarabun', normal='THSarabun', bold='THSarabun-Bold')
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ===== Header =====
    logo_path = os.path.join(settings.MEDIA_ROOT, 'ImageUserProfile/cropped-LOGO-2.png') 
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 2 * cm, height - 8 * cm, width=2*cm, preserveAspectRatio=True, mask='auto')

    p.setFont("THSarabun-Bold", 22)
    p.setFillColor(colors.HexColor('#003366'))
    p.drawString(4.5 * cm, height - 2.5 * cm, "รายงานการเบิกอะไหล่ซ่อมคอมพิวเตอร์")
    p.drawString(4.5 * cm, height - 3.2 * cm, "กลุ่มงานสุขภาพดิจิทัล สสจ.กระบี่")

    p.setStrokeColor(colors.black)
    p.setLineWidth(0.5)
    p.line(2 * cm, height - 4.2 * cm, width - 2 * cm, height - 4.2 * cm)

    p.setFont("THSarabun-Bold", 18)
    p.setFillColor(colors.black)
    p.drawString(2 * cm, height - 4.8 * cm, f"วันที่: {item.created_at.strftime('%d/%m/%Y %H:%M')}")

    # ===== รายละเอียดอะไหล่ =====
    y = height - 6 * cm
    line_height = 1 * cm

    def draw_line(label, value):
        nonlocal y
        p.setFont("THSarabun-Bold", 18)
        p.setFillColor(colors.black)
        p.drawString(2 * cm, y, f"{label}:")
        p.drawString(8 * cm, y, str(value))
        y -= line_height
    
    # วาด barcode สำหรับหมายเลขใบเบิกอะไหล่
    def draw_barcode(value):
        barcode_obj = code128.Code128(value, barWidth=0.8, barHeight=15, quietZone=20)  # สร้าง barcode
        barcode_obj.drawOn(p, 7 * cm, y - 1)  # วาด barcode ในตำแหน่งที่ต้องการ
        return barcode_obj.height  # คืนค่าความสูงของ barcode เพื่อใช้ในการเลื่อนตำแหน่ง

    # วาดข้อมูล
    y -= draw_barcode(item.repair_id)  # สร้าง barcode สำหรับหมายเลขใบเบิกอะไหล่
    draw_line("หมายเลขใบเบิกวัสดุ", item.repair_id)
    draw_line("หมายเลขครุภัณฑ์คอมพิวเตอร์", item.computer_id  )
    draw_line("ชื่อวัสดุซ่อม/รายละเอียด", item.part_id)
    draw_line("หมายเลขซีเรียล", item.part_sn or "-")
    draw_line("จำนวนที่เบิก(ชิ้น)", item.part_amount_use)
    draw_line("ผู้สั่งเบิก", user_order.user.get_full_name() if user_order else "N/A")
    draw_line("ผู้บันทึกข้อมูล", admin_recorder.user.get_full_name() if admin_recorder else "N/A")

    p.setStrokeColor(colors.black)
    p.setLineWidth(0.5)
    p.line(2 * cm, height - 15 * cm, width - 2 * cm, height - 15 * cm)

    # ===== หมายเหตุ =====
    remark_text = "ไม่มีหมายเหตุ"  # หากมีหมายเหตุให้เพิ่มจาก model
    p.setFont("THSarabun-Bold", 16)
    p.drawString(2 * cm, y, "หมายเหตุ:")
    p.setFont("THSarabun", 16)
    p.drawString(4 * cm, y, remark_text)
    y -= line_height

    # ===== รูปภาพประกอบ =====
    if images.exists():
        p.setFont("THSarabun-Bold", 16)
        p.drawString(2 * cm, y, "รูปภาพประกอบ:")
        y -= 2 * cm

        for img in images:
            image_path = os.path.join(settings.MEDIA_ROOT, str(img.repair_image))
            if os.path.exists(image_path):
                try:
                    p.drawImage(image_path, 2 * cm, y - 6 * cm, width=10 * cm, height=6 * cm, preserveAspectRatio=True, mask='auto')
                    y -= 7 * cm
                    if y < 7 * cm:
                        p.showPage()
                        y = height - 3 * cm
                except Exception as e:
                    p.drawString(2 * cm, y, f"แสดงภาพไม่สำเร็จ: {str(e)}")
                    y -= 1 * cm

    # ===== ลายเซ็น =====
    if y < 6 * cm:
        p.showPage()
        y = height - 3 * cm

    # เว้นระยะด้านบน
    y -= 2 * cm
    p.setFont("THSarabun", 16)

    # ลายเซ็นซ้าย (ผู้บันทึกข้อมูล)
    left_x = width * 0.25
    p.drawCentredString(left_x, y, "ลงชื่อ ..........................................................")
    p.drawCentredString(left_x, y - 1 * cm, f"( {admin_recorder.user.get_full_name() if admin_recorder else ''} )")
    p.drawCentredString(left_x, y - 2 * cm, "ผู้บันทึกข้อมูล")

    # ลายเซ็นขวา (ผู้รับวัสดุ)
    right_x = width * 0.75
    p.drawCentredString(right_x, y, "ลงชื่อ ..........................................................")
    p.drawCentredString(right_x, y - 1 * cm, "(...............................................)")
    p.drawCentredString(right_x, y - 2 * cm, "ผู้รับวัสดุ")
    # ===== QR Code =====
    qr_url = request.build_absolute_uri(f"/repair_order_pdf/{pk}/pdf")
    qr = qrcode.make(qr_url)
    qr_io = BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)

    # แปลง BytesIO เป็น ImageReader
    qr_image_reader = ImageReader(qr_io)

    # ใช้ ImageReader ในการแสดง QR Code
    p.drawImage(qr_image_reader, 2 * cm, y - 5 * cm, width=2 * cm, height=2 * cm)

    # ข้อความใต้ QR Code
    p.setFont("THSarabun", 12)
    p.drawString(2 * cm, y - 5.5 * cm, "สแกน QR Code เพื่อดูรายงานออนไลน์")

    # Footer with page number
    p.setFont("THSarabun", 14)
    p.setFillColor(colors.gray)
    p.showPage()
    p.save()

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
    response['Content-Disposition'] = f'inline; filename="repair_report_{item.repair_id}.pdf"'
    return response
