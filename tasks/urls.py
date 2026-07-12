
from django.urls import path , include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('add_task/', views.add_task, name='add_task'),
    path("complete/<int:id>/", views.mark_complete, name="mark_complete"),
    path("edit-task/<int:id>/", views.edit_task, name="edit_task"),
    path("pending/<int:id>/", views.mark_pending, name="mark_pending"),
    path("delete-task/<int:id>/", views.delete_task, name="delete_task"),
]
