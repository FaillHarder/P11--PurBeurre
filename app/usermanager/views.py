from usermanager.forms import SignUpForm, ImageProfileForm
from usermanager.models import User, ImageProfile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

import os
from pathlib import Path


class Signup(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = SignUpForm


class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    next_page = reverse_lazy('index')


class Profile(LoginRequiredMixin, TemplateView):
    form_class = ImageProfileForm
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context['username'] = Profile.extract_username_from_mail(
            str(self.request.user).title()
        )
        context['email'] = self.request.user
        user = self.request.user.pk
        try:
            avatar_profile = ImageProfile.objects.get(user_id=user)
            context['avatar'] = avatar_profile
        except ObjectDoesNotExist:
            context['avatar'] = 0
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    @staticmethod
    def extract_username_from_mail(mail):
        return mail[:mail.find('@')]

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('img_profile')
            user = request.user
            Profile.try_if_user_img_exist_and_delete_or_create(img, user)
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def try_if_user_img_exist_and_delete_or_create(img, user):
        try:
            img_exist = ImageProfile.objects.get(user_id=user.pk)
            img_path = Path("media/{}".format(img_exist.img_profile))
            if img_path.is_file():
                os.remove("media/{}".format(img_exist.img_profile))
            img_exist.img_profile = img
            img_exist.save()
        except ObjectDoesNotExist:
            ImageProfile.objects.create(
                img_profile=img,
                user=user
            )
