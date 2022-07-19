from django.urls import path
from app.views import *

urlpatterns = [
    path('', home ,name='home'),
    path('signup', signup ,name='signup'),
    path('Logout', Logout ,name='Logout'),

    # Admin

    path('adminlogin', adminlogin ,name='adminlogin'),
    path('adminregister', adminregister ,name='adminregister'),
    path('adminhome', adminhome ,name='adminhome'),
    path('admprofile',admprofile,name='admprofile'),
    path('admin_studetails',admin_studetails,name='admin_studetails'),
    path('staffdetails',staffdetails,name='staffdetails'),
    path('admin_viewstudetails/<int:pid>', admin_viewstudetails,name='admin_viewstudetails'),
    path('admin_viewstaff/<int:pid>', admin_viewstaff,name='admin_viewstaff'),
    path('deletestaff/<int:pid>', deletestaff,name='deletestaff'),
    path('admin_addstu',admin_addstu,name='admin_addstu'),
    path('admin_addstaff',admin_addstaff,name='admin_addstaff'),





    # Staff

    path('stafflogin', stafflogin ,name='stafflogin'),
    path('staffregister', staffregister ,name='staffregister'),
    path('staffhome', staffhome ,name='staffhome'),
    path('staffprofile',staffprofile,name='staffprofile'),
    path('classes', classes ,name='classes'),
    path('staff_studetails',staff_studetails,name='staff_studetails'),
    path('staff_addstu', staff_addstu ,name='staff_addstu'),
    path('view_studetails/<int:pid>', view_studetails,name='view_studetails'),
    path('staff_deletestu/<int:pid>', staff_deletestu,name='staff_deletestu'),
    path('staff_viewattendance/<str:pid>',staff_viewattendance,name='staff_viewattendance'),
    path('staff_startattendance/<str:pid>',staff_startattendance,name='staff_startattendance'),





    # Students

    path('studenlogin', studentlogin ,name='studentlogin'),
    path('sturegister', sturegister ,name='sturegister'),
    path('stuhome', stuhome ,name='stuhome'),
    path('stuprofile',stuprofile,name='stuprofile'),
    path('stu_markattendance/<str:pid>',stu_markattendance,name='stu_markattendance'),
    path('stu_viewattendance/<str:pid>',stu_viewattendance,name='stu_viewattendance'),



]
