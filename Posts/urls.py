from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),

    path('new/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),

    path('react/<int:post_id>/<str:reaction_type>/', views.add_reaction, name='add_reaction'),

    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]