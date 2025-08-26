# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def split(value, delimiter=" "):
	return value.split(delimiter)


@register.filter
def thai_date(value):
	if not value:
		return ''
	try:
		thai_year = value.year + 543
		return value.strftime(f'%d/%m/{thai_year}')
	except:
		return value
		