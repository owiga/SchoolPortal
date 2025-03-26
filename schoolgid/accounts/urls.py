from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('teacher_register/', views.teacher_register, name='teacher_register'),
    path('login/', views.login_user, name='login_user'),
    path('<str:username>/filter_users/', views.filter_users, name='filter_users'),
    path('<str:username>/', RedirectView.as_view(pattern_name='profile', permanent=False)),
    path('<str:username>/main/', views.profile, name='profile'),
    path('<str:username>/friends/', RedirectView.as_view(pattern_name='friends', permanent=False)),
    path('<str:username>/friends/list', views.friends, name='friends'),
    path('<str:username>/friends/request', views.friend_request, name='friend_request'),
    path('<str:username>/friends/sended', views.sended, name='sended'),
    path('<str:username>/friends/accept_friend_request/<int:user_id>', views.accept_friend_request, name='accept_friend_request'),
    path('<str:username>/friends/reject_friend_request/<int:user_id>', views.reject_friend_request, name='reject_friend_request'),
    path('<str:username>/grades/', views.grades, name='grades'),
    path('<str:username>/add_grades/', views.add_grades, name='add_grades'),
    path('<str:username>/school_card/', views.school_card, name='school_card'),
    path('<str:username>/settings/profile', views.setting_profile, name='settings'),
    path('<str:username>/settings/confidentiality', views.confidentiality, name='confidentiality'),
    path('<str:username>/settings/site-settings', views.site_settings, name='site-settings'),
    path('<str:username>/send_friend_request/<int:user_id>', views.send_friend_request, name='send_friend_request'),
    path('<str:username>/cancel_friend_request/<int:user_id>', views.cancel_friend_request, name='cancel_friend_request'),
    path('<str:username>/delete_friend/<int:user_id>', views.delete_friend, name='delete_friend'),
]