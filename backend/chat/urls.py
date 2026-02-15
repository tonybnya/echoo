"""
Script Name : urls.py
Description : URL's for the chat app
Author      : @tonybnya
"""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('chats/', views.ChatSessionView.as_view()),
    path('chats/<str:uri>/', views.ChatSessionView.as_view()),
    path('chats/<str:uri>/messages/', views.ChatSessionMessageView.as_view())
]