
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/',views.about_view,name='about'),
    path('contact/',views.contact_view,name='contact'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('signup/',views.signup_view,name='signup'),
    path('animation/',views.animation_view,name='animation'),
    path('handgestures/', views.handgestures_view, name='handgestures'),
    path('spanish/',views.spanish_view,name='spanish'),
    path('french/',views.french_view,name='french'),
    path('arabic/',views.arabic_view,name='arabic'),
    path('korean/',views.korean_view,name='korean'),
    path('german/',views.german_view,name='german'),
    path('japanese/',views.japanese_view,name='japanese'),
    path('hindi/',views.hindi_view,name='hindi'),
    path('telugu/',views.telugu_view,name='telugu'),
    path('urdu/',views.urdu_view,name='urdu'),
    path('',views.home_view,name='home'),
    path('animation/',views.animation_view,name='animation'),
    path('spanish/',views.spanish_view,name='spanish'),
    path('animation/',views.animation_view,name='animation')
]
