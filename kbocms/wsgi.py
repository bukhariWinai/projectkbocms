"""
WSGI config for kbocms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
# ------------ when use  localhost--------------
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kbocms.settings')

application = get_wsgi_application()

#####--------------when use productions server-------------------#####


# import os
# import sys
# import site

# #  แก้ตรงนี้ให้เป็น path ไปยัง virtualenv ของคุณจริง ๆ
# VENV_PATH = '/home/kbocmsadmin/venv'
# VENV_PATH = '/home/kbocms/venv'

# # เพิ่ม site-packages ของ venv เข้ามา
# site.addsitedir(f'{VENV_PATH}/lib/python3.10/site-packages')  # แก้ python3.10 ให้ตรงเวอร์ชันคุณ

# # เพิ่ม path สำหรับ python binary ด้วย (optional)
# sys.path.insert(0, os.path.join(VENV_PATH, 'bin'))

# # Django settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kbocms.settings')

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
# ####--------------------when use productions server---------------####