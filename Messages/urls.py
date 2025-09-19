from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('new/', views.new_conversation, name='new_conversation'),
]

