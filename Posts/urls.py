from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]