from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('profile/', views.user_profile, name='profile'),
]
