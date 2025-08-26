from django.urls import path,include
from .views import *

urlpatterns = [
    
    
    path('', Home, name='home_page'),
    
    #path('itadmin/',ItAdmin, name= 'itadmin_page'),


    path('news/',NewsShow, name='news_page'),

    path('newsdetails/<int:news_id>/',NewsDetails, name='newsdetails_page'), #new

    path('postdetails/<int:serviceid>/',PostDetails, name='postdetails_page'),
    path('docdetails/<int:doc_id>/',DocDetails, name='docdetails_page'),

    path('office_center/',ProgramOfficeView, name='office_center_page'),
    path('anounce/',Anounce, name = 'anounce_page'), #ข่าวประกาศ รับสมัครงาน หรือ ย้ายงาน หรือ ประกวดราคา
    path('conference/',ConferenceView, name = 'conference_page'),    
    path('confschedule/<int:confid>/',ConfScheduleView, name = 'confschedule_page'),        
    path('contact/',Contact, name = 'contact_page'),
    path('download/',Download, name = 'download_page'),
    path('formdownload/',FormDownload, name = 'formdownload_page'),
    path('promote/',Promote, name = 'promote_page'),#ข่าว catagory ประชาสัมพันธ์
    path('section/',Section, name = 'sections_page'),
    path('services/',Services, name= 'services_page'),
    path('comrequest/',Comrequest, name= 'comrequest_page'),
    path('cyberpolicy/',CyberPolicy, name= 'cyberpolicy_page'),
    path('onepage/',OnePages, name= 'onepages_page'),
    path('onepagedetail/<int:op_id>/',OnePageDetail, name= 'onepagedetail_page'),

    path('policy_detail/<int:policyid>/',CyberPolicyDetail, name= 'cyberpolicydetail_page'),
    path('cyberimpect_detail/<int:cyberimpectid>/',CyberImpectDetail, name= 'cyberimpectdetail_page'),
    #frontendform
    #path('addnewsform/',AddNewsForm, name= 'addnewform_page'),

]
