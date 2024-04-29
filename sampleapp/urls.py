
from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index, name="index"),
    path('',views.index, name="index"),
    path('contact/',views.contact, name="contact"),
    path('about/',views.about, name="about"),
    path('service/',views.service, name="service"),
    path('register/',views.register, name="register"),
    path('adminreg/',views.adminregister,name='admin_register'),
    path('admlog/',views.admlog,name='admlog'),
    path('login/',views.login, name="login"),
    path('home/',views.home, name="home"),
    path('admhome/',views.admhome,name='admhome'),
    path('logout/',views.logoutc,name="logout"),
    path('profile/',views.profile,name='profile'),
    path('proupdate/',views.proupdate,name='proupdate'),
    path('userlist/',views.userlist,name='userlist'),
    path('agentreg/',views.agentreg,name='agentregister'),
    path('agenthome/',views.agenthome,name='agenthome'),
    path('agentlogin/',views.agentlog, name="agentlogin"),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('uploadform/',views.uploadform,name='uploadform'),
    path('listpatient/',views.listpatient,name='listpatient'),
    path('patientlistviewforagent/',views.patientlistviewforagent,name='patientlistviewforagent'),
    path('search/',views.search,name='search'),
    path('adpatient/',views.adpatient,name='adpatient'),
    path('deletes/<int:id>/',views.deletes,name='deletes'),
    path('import-csv/', views.import_csv, name='import_csv'),
    path('agentlist/', views.agentlist, name='agentlist'),
    path('patientview/<str:agemail>/', views.patientview, name='patientview'),
    path('viewbyid/',views.viewbyid,name='viewbyid'),
    path('patientviewbyid/',views.patientviewbyid,name='patientviewbyid'),
    path('patientviewbyid2/',views.patientviewbyid2,name='patientviewbyid2'),
    path('deletepatient/<int:id>/',views.deletepatient,name='deletepatient'),
    path('approve-reject-agent/', views.approve_reject_agent, name='approve_reject_agent'),
    # path('prediction/', views.save_prediction_result, name='save_prediction_result'),
    

    

]