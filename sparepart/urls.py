from django.urls import path,include
from sparepart.views import *



urlpatterns = [
	# path ('addstockparts/',AddStockParts, name='addstockparts_page'),
	# path ('take_a_parts/',Take_A_Parts, name='take_a_parts_page'),
	# path ('addpartstype/',AddPartsType, name='addpartstype_page'),
	# path ('alltake_a_parts/',AllTake_A_Parts, name='alltake_a_parts_page'),
	path ('servermainten/',ServerMainten, name='servermainten_page'),

]
