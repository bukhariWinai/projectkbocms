# cmsapp_backend/utils/alerts.py

from django.urls import reverse
from django.http import HttpResponse

def somethingwrong_alert(message, title="เกิดข้อผิดพลาด", icon="error", redirect_url_name="home_page"):
    """
    ส่งกลับ HttpResponse HTML ที่ฝัง SweetAlert2 และ redirect ไปหน้าอื่น

    :param message: ข้อความใน alert
    :param title: หัวข้อใน alert
    :param icon: ประเภท icon เช่น 'error', 'warning', 'success'
    :param redirect_url_name: ชื่อ URL name ที่จะ redirect ไป
    :return: HttpResponse HTML
    """
    url = reverse(redirect_url_name)
    return HttpResponse(f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        </head>
        <body>
            <script>
                Swal.fire({{
                    icon: '{icon}',
                    title: '{title}',
                    text: '{message}',
                    confirmButtonText: 'ตกลง'
                }}).then((result) => {{
                    window.location.href = '{url}';
                }});
            </script>
        </body>
        </html>
    """)
