from django.urls import path

from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
]
