from django.urls import path,include
from .views import *
from server_mainten.views import *
from vdoconf_conclusion.views import *
from sparepart.views import *

from .views import load_subcategories_bkend


urlpatterns = [
    path ('homeconf/',Homeconf, name='homeconf_page'),
    path ('allconf/',Allconf, name='allconf_page'),
    path ('confdetails/<int:conf_id>/ConfDetails/',ConfDetails, name='confdetails_page'),
    path ('addserver/',AddSerVer, name='addserver_page'),
    path ('servermainten/',ServerMainten, name='servermainten_page'),
    path ('itemservermainten/',ItemServerMainten, name='itemservermainten_page'),
    path ('servermaintendetails/<int:mainten_id>/ServerMaintenDetails/',ServerMaintenDetails, name='servermaintendetails_page'),    
    #path('', Home, name='home_page'),
    path('register/',Register, name= 'register_page'),    
    path('itadmin/',ItAdmin, name= 'itadmin_page'),
    path('addnewsform/',AddNewsForm, name= 'addnewform_page'),
    path('addartical/',AddArtical, name= 'addartical_page'),
    path('addconference/',AddConference, name= 'addconference_page'),
    path('addourservice/',AddOurService, name= 'addourservice_page'),
    path('addoffice_center/',AddOfficeCenter, name= 'addofficecenter_page'),
    #path('doanythings/',DoAnyThings, name= 'doanythings_page'),GPHSection
    path('addfiledownload/',AddFileDownload, name= 'addfiledownload_page'),
    path('headersetting/',HeaderSetting, name= 'headersetting_page'),
    path('footersetting/',FooterSetting, name= 'footersetting_page'),
    path('showcomreq/',ShowComReq, name= 'showcomreq_page'),
    path('userprofile/',UserProfile, name= 'userprofile_page'),
    path('updateprofile/<int:userprofile_id>/UpdateProfile/',UpdateProfile, name= 'updateprofile_page'),
    path('updateprofileuseradmin/<int:user_id>/UpdateProfileUserAdmin/',UpdateProfileUserAdmin, name= 'updateprofileUseradmin_page'),
    path('showalluser/',ShowAllUser, name= 'showalluser_page'),

    path('registrainee/',AddTrainee, name= 'addtrainee_page'),
    path('showtrainee/',ShowTrainee, name= 'showtrainee_page'),
    path('showalltrainee/',ShowAllTrainee, name= 'showalltrainee_page'),
    path('traineedetails/<int:trainee_id>/TraineeDetails/',TraineeDetails, name= 'traineedetails_page'),
    
    path('showallrepair/',ShowAllRepair, name= 'showallrepair_page'),
    path('showdevicerepair/<int:showrepaired_id>/ShowDeviceRepair/',ShowDeviceRepair, name= 'showdevicerepair_page'),

    path('repairresultsave/<int:item_id>/RepairResultSave/',RepairResultSave, name= 'repairresultsave_page'),
    path('repairresultupdate/<int:item_id>/RepairResultUpdate/',RepairResultUpdate, name= 'repairresultupdate_page'),
    path('repairreport/<int:item_id>/RepairReport/',RepairReport, name= 'repairreport_page'),

    path('borrowdevicesave/',BorrowDeviceSave, name= 'borrowdevicesave_page'),
    path('showallborrow/',ShowAllBorrow, name= 'showallborrow_page'),
    path('borrowedit/<int:item_id>/BorrowEdit/',BorrowEdit, name= 'borrowedit_page'),
    path('borrowreturn/<int:item_id>/EditBorrowReturn/',EditBorrowReturn , name= 'borrowreturn_page'),   
    path('borrowreport/<int:item_id>/BorrowReport/',BorrowReport, name= 'borrowreport_page'),
    path('deviceprofile/',DeviceProfile, name= 'deviceprofile_page'),
    path('computerdetails/<int:com_id>/ComputerDetails/',ComputerDetails, name= 'computerdetails_page'),
    path('computerupdatedetails/<int:item_id>/ComputerUpdateDetails/',ComputerUpdateDetails, name='computerupdatedetails_page'),
    path('fontaweasome/',FontAweasome, name= 'fontaweasome_page'),
    path('newscategory/',NewsCategorybk, name= 'newscategory_page'),
    path('sectionbk/',Sectionbk, name= 'sectionbk_page'),
    path('adsbanner/',AdsBanner, name= 'adsbanner_page'),
    path('external-link/',ExternalLink, name= 'external-link_page'),
    path('onepagebk/',Onepagebk, name= 'onepagebk_page'),

    path('com_management/',ComputerManagement, name= 'com_management_page'),
    path('showalldevices/',ShowAllDevices, name= 'showalldevices_page'),
   
    path('add_rapair/<int:repair_id>/AddRepair/',AddRepair, name= 'add_repairing_page'),

    path('cyber_policy/',AddCyberPolicy, name= 'addcyberpolicy_page'),
    path('cybersecurity_management/',CyberSecurityManagement, name= 'cybersecurity_management_page'),    
    path('addworkreport/',AddWorkReport, name= 'addworkreport_page'),    
    path('allworkreportview/',AllWorkReportView, name= 'allworkreportview_page'),
    path('workreportdetail/<int:work_id>/WorkReportDetail/',WorkReportDetail, name= 'workreportdetail_page'),    
    path('workratingtrainee/<int:work_id>/RatingWorkingTrainee/',RatingWorkingTrainee, name= 'workratingtrainee_page'),    
    path('ShowAllReportView/',ShowAllReportView, name= 'ShowAllReportView_page'),    

    path('update_success/',Update_success, name= 'update_success_page'),    

    path('mainspareparts/',MainSpareParts, name='mainspareparts_page'),    
    path ('addstockparts/',AddStockParts, name='addstockparts_page'),
    path ('take_a_parts/',Take_A_Parts, name='take_a_parts_page'),
    path ('addpartstype/',AddPartsCat, name='addpartstype_page'),   
    path ('alltake_a_parts/',AllTake_A_Parts, name='alltake_a_parts_page'),

    path ('addpartsub/',AddPartSub, name='addpartsub_page'),

    path('load-subcategories/', Load_Subcategories, name='load_subcategories_page'),
    path('load-subcategories_bkend/', load_subcategories_bkend, name='load_subcategories_bkend_page'),
    
    path('repair_order_pdf/<int:pk>/pdf/',Generate_repair_pdf , name='repair_order_pdf_page'),
    path("generate_qr_pdf/<str:cp_id>/pdf", Generate_Qr_Pdf, name="generate_qr_pdf"),
    path('export_consent/<int:cp_id>/pdf', ExportConsentPdf, name='export_consent_pdf'),
    path('export_returndevice/<int:cp_id>/pdf', ExportReturnDevicePdf, name='export_returndevice_pdf'),
    path('export_workreport/<int:wr_id>/pdf', ExportWorkReportPdf, name='workreport_pdf'),
    
    path('userprint/<int:user_id>/pdf', Generate_UserProfile_Pdf, name='userprint_pdf'),
    # path("export_workreport_pdf/<int:wr_id>/pdf", Export_Workreport_Pdf, name="export_workreport_pdf"),


    


]
