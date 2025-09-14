from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete/<int:post_id>/', views.delete_post, name='admin_delete_post'),
    path('ban/<str:username>/', views.ban_user, name='ban_user'),
    path('unban/<str:username>/', views.unban_user, name='unban_user'),

]