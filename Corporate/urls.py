from django.urls import path
from .views import Register,LoginView,LogoutView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name="Corporate-index"),
    path('register/',Register.as_view(),name = "Corporate-register"),
    path('login/',LoginView.as_view(),name="Corporate-login"),
    path('logout/',LogoutView.as_view(),name="Corporate-logout"),
    path('reset-password/',auth_views.PasswordResetView.as_view(template_name="Corporate/resetPassword.html"),name="password_reset_Corporate"),
    path('reset-password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="Corporate/resetPasswordSent.html"),name="Corporate"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="Corporate/setNewPassword.html"),name="Corporate"),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="Corporate/resetPasswordDone.html"),name="password_reset_complete_Corporate"),
]
