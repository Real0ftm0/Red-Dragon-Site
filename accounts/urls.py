from django.urls import path 
from accounts import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    #singup 
    path('login/',views.login_view,name='login'),
    path('signup/', views.signup_view, name = 'signup'),

    # Email Confirmation View
    path('ConfirmEmail/', views.ConfirmEmail.as_view(), name='confirm_email'),

    # Profile View
    path('profile/', views.EditProfileView.as_view(), name='profile'),

    # Forgot / Reset Password View
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/reset_password.html'),
        name='password_reset',
        ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'),
        name='password_reset_done',
        ),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'),
        name='password_reset_confirm',
        ),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'),
        name='password_reset_complete',
        ),
]