from django.urls import path
from django.contrib.auth import views as auth_views
from members import views as members_views
app_name = 'members'

urlpatterns = [
    path('accounts/login/', members_views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/signup/', members_views.SignupCreateView.as_view(), name='signup'),
    # path('accounts/profile/<int:pk>/edit/', members_views.EditProfileView.as_view(), name='edit_profile'),
    # path('accounts/profile/<int:pk>/page/', members_views.ShowProfileView.as_view(), name='view_profile_page'),
    # path('accounts/password/', members_views.EditPasswordView.as_view(), name='pass_change'),
    # path('accounts/password-change/success/', members_views.PasswordChangeSuccessView.as_view(), name='pass_success'),
]
