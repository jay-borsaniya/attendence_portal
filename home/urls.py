from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path("user_login/", views.user_login, name="user_login"),
    path("apply_leave/", views.apply_leave, name="apply_leave"),
    path("applied_leaves/", views.applied_leaves, name="applied_leaves"),
    path("cancelled_leaves/<int:leave_id>", views.cancelled_leaves, name="cancelled_leaves"),
    path("change_password/", views.change_password, name="change_password"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("punch_in/", views.punch_in, name="punch_in"),
    path("punch_out/", views.punch_out, name="punch_out"),
]
