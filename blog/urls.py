from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/create_ticket', views.create_ticket, name='create_ticket'),
    path('/modify_ticket/<int:_id>', views.modify_ticket, name='modify_ticket'),
    path('/create_review', views.create_review, name='create_review'),
    path('/modify_review/<int:_id>', views.modify_review, name='modify_review'),
    path('/post', views.post, name='post'),
    path('/logout', views.logout_request, name='logout'),
    path('/delete_ticket/<int:_id>', views.delete_ticket, name='delete_ticket')
]

