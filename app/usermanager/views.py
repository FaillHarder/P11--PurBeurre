from usermanager.forms import SignUpForm, ImageProfileForm
from usermanager.models import User, ImageProfile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

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


class Profile(LoginRequiredMixin, FormView):
    form_class = ImageProfileForm
    template_name = 'profile.html'
    permission_required = 'usermanager.Login'

    def get_context_data(self):
        context = super().get_context_data()
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
            # delete old image
            os.remove(Path(f"media/{img_exist}"))
            img_exist.img_profile = img
            img_exist.save()
        except ObjectDoesNotExist:
            ImageProfile.objects.create(
                img_profile=img,
                user=user
            )
