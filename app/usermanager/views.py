from usermanager.forms import SignUpForm, ImageProfileForm
from usermanager.models import User, ImageProfile

import os
from pathlib import Path
from django.views.generic import CreateView, TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class Signup(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = SignUpForm


class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    next_page = reverse_lazy('index')


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    permission_required = 'usermanager.Login'

    def get_context_data(self):
        context = super().get_context_data()
        context['username'] = Profile.extract_username_from_mail(
            str(self.request.user)
        )
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


def customize(request):

    if request.method == 'POST':
        form = ImageProfileForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('img_profile')
            user = request.user
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
            return redirect('profile')
    else:
        form = ImageProfileForm()
    return render(request, 'customize.html', {'form': form})
