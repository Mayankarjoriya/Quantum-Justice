from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns =[
    # path('', include('users.urls')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('client-page/', views.client_page, name='client-page'),
    path('lawyer-page/', views.lawyer_page, name='lawyer-page'),
    path('search-lawyers/', views.search_lawyer, name='search-lawyers'),

]