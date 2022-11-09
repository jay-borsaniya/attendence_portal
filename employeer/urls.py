from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('requests/', views.requests, name="requests"),
    path('new_employee/', views.new_employee, name="new_employee"),
    path('approve_leave/<int:leave_id>', views.approve_leave, name="approve_leave"),
    path('reject_leave/<int:leave_id>', views.reject_leave, name="reject_leave"),
]
