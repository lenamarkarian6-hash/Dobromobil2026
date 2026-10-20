from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('direction/<slug:slug>/', views.direction_detail, name='direction_detail'),
    path('map/', views.map_view, name='map'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/enroll/', views.enroll, name='enroll'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('reports/', views.reports, name='reports'),
]
