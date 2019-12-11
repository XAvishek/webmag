from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts import views

urlpatterns = [

    path('login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="index.html"), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('subscribe/', views.email_list_user, name='subscribe'),

] 
