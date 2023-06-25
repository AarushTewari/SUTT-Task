from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'hospital'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.patient_login, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('change_profile', views.changeprofile, name='changeprofile'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('patient_appointments', views.patient_appointments, name='patient_appointments'),
    path('staff_login', views.staff_login, name='staff_login'),
    path('logout', views.Logout, name='logout'),
    path('staffwelcome', views.welcomestaff, name='welcomestaff'),
    path('add_appointment', views.add_appointment, name='add_appointment'),
    path('view_appointment', views.view_appointment, name='view_appointment'),
    path('see_appointment/<int:id>', views.see_appointment, name='see_appointment'),
    path('change_appointment/<int:id>', views.change_appointment, name='change_appointment'),
    path('search/', views.search_patients, name='search_users'),
    path('chatrooms', views.chatrooms, name='chatrooms'),
    path('createroom', views.createroom, name='createroom'),
    path('chatrooms/<str:patient>', views.room, name='room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:patient>/', views.getMessages, name='getMessages'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard')    
]
