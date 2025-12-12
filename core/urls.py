from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('habit/<int:habit_id>/', views.habit_detail, name='habit_detail'),
    path('habit/<int:habit_id>/update/', views.update_habit, name='update_habit'),
    path('habit/<int:habit_id>/delete/', views.delete_habit, name='delete_habit'),
    path('create-habit/', views.create_habit, name='create_habit'),
    path('toggle-checkin/', views.toggle_checkin, name='toggle_checkin'),
    path('settings/', views.settings, name='settings'),
]
