#custom_tags.py on cmsapp frontend

from django	import template
from ..models import *

register = template.Library()

@register.simple_tag #this gramma
def hello_tag(): # Bring and take this tag paste all pages html in your project
	return	'ยินดีต้อนรับ สำนักงานสาธารณสุขจังหวัดกระบี่' 

@register.simple_tag #this gramma
def count_all_news():
	all_news = News.objects.count()
	return all_news

@register.simple_tag #this gramma
def count_all_repair():
	all_repair = RepairAndPartChange.objects.count()
	return all_repair

@register.simple_tag
def count_com_request():
	com_request = ComRequest.objects.count()
	return com_request

@register.simple_tag
def link_external():
	link = LinkExternal.objects.get.all()[:5].order_by('id')
	return link


@register.simple_tag
def last_news():
	lastnews = News.objects.all()[:5].order_by('id')
	return lastnews
