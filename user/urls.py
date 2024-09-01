from django.urls import path
from . import views

urlpatterns=[
     
    path('',views.timetable_view,name='timetable_view'),

    path('timetable_view',views.timetable_view,name='timetable_view'),

    path('login',views.login,name='login'),

    path('admin_register',views.admin_register,name='admin_register'),

    path('logout',views.logout,name='logout'),
    
    path('change_password',views.change_password,name='change_password'),

    path('forgot',views.forgot,name='forgot'),

    path('faculty_login',views.faculty_login,name='faculty_login'),

    path('view_fac',views.view_fac,name='view_fac'),

    path('dashboard_f',views.dashboard_f,name='dashboard_f'),

    path('faculty_reg',views.faculty_reg,name='faculty_reg'),

    path('logoutf',views.logoutf,name='logoutf'),

    path('forgotf',views.forgotf,name='forgotf'),

    path('index',views.index,name='index'),

    path('depmanage',views.depmanage,name='depmanage'),

    path('add_dep',views.add_dep,name='add_dep'),

    path('del_dep/<str:bname>/',views.del_dep,name='del_dep'),

    path('edit_dep/<str:bname>/',views.edit_dep,name='edit_dep'),

    path('subject',views.subject,name='subject'),

    path('add_sub',views.add_sub,name='add_sub'),

    path('del_sub/<str:subid>/',views.del_sub,name='del_sub'),

    path('edit_sub/<str:subid>/',views.edit_sub,name='edit_sub'),

    path('faculty',views.faculty,name='faculty'),

    path('add_fac',views.add_fac,name='add_fac'),

    path('del_fac/<str:fsid>/',views.del_fac,name='del_fac'),

    path('edit_fac/<str:fsid>/',views.edit_fac,name='edit_fac'),

    path('create_tt',views.create_tt,name='create_tt'),

    path('gen_tt',views.gen_tt,name='gen_tt'),

    path('view_gen_tt',views.view_gen_tt,name='view_gen_tt'),

    path('view_tt',views.view_tt,name='view_tt')
    ]

    
    
    






