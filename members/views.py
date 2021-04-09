from django.views.generic import CreateView, UpdateView, TemplateView, DetailView, ListView
from members.forms import LoginForm, SignupForm, EditProfileForm, PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


class UserLoginView(LoginView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:  # if a user with entered username and password is found:
                login(request, user)
                messages.success(request, f'{username}, you have lodged in successfully')
                return redirect('mysite:show-all-tasks')
            else:
                # user not found: either password or username are not found
                messages.error(request, "Invalid username or password")
                return render(request, 'registration/login.html', {'form': form})
                # I used render instead of redirect because i wanted to show the previous
                # entered username using form.is_bound

        else:
            messages.error(request, "Invalid username or password")
            return redirect('members:login')


# class EditPasswordView(PasswordChangeView):
#     form_class = PasswordResetForm
#     template_name = 'registration/change_password.html'
#     success_url = reverse_lazy('accounts:pass_success')
#
#
# class SignupCreateView(CreateView):
#     form_class = SignupForm
#     template_name = 'registration/signup.html'
#     success_url = reverse_lazy('accounts:login')
#
#
# class EditProfileView(UpdateView):
#     model = User
#     form_class = EditProfileForm
#     template_name = 'registration/edit_profile.html'
#     success_url = reverse_lazy('questions:all_questions')
#
#
# class PasswordChangeSuccessView(TemplateView):
#     template_name = 'registration/change-pass-success.html'
#
#
# class ShowProfileView(DetailView):
#     model = User
#     template_name = 'accounts/profile_page.html'


# class NotificationView(ListView):
#     model = Notification
#     template_name = 'accounts/all_notifications.html'