from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from django.conf import settings

from .forms import UserRegisterForm, UserLoginForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        self.send_welcome_email(user)

        return HttpResponseRedirect(self.success_url)

    def send_welcome_email(self, user):
        subject = 'Добро пожаловать в Skystore!'
        message = f'''
        Уважаемый(ая) {user.first_name or 'пользователь'}!

        Добро пожаловать в Skystore - лучший магазин цифровых продуктов!

        Мы рады приветствовать вас в нашем сообществе.

        С уважением,
        Команда Skystore
        '''
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('catalog:home')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user