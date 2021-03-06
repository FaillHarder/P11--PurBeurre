from usermanager.forms import ImageProfileForm
from usermanager.models import User, ImageProfile
from usermanager.views import Profile

from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.urls import reverse
import os


# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.username = "usernametest@test.fr"
        self.password = "passwordtest"
        self.username2 = "usernametest2@test.fr"
        User.objects.create(
            email=self.username,
            password=self.password
        )
        self.user = User.objects.get(email=self.username)

        self.image = SimpleUploadedFile(
            name='test.png',
            content=open("static/assets/img/avatar.png", 'rb').read(),
            content_type='image/png'
        )

        return super().setUp()

    def test_signup_class_view(self):
        response_get = self.client.get(reverse("signup"))
        self.assertContains(response_get, "Créer un compte", status_code=200)

    def test_signup_post_with_good_information(self):
        response_post = self.client.post(reverse("signup"), {
                "email": self.username2,
                "password1": self.password,
                "password2": self.password
            },
            follow=True
        )
        self.assertContains(
            response_post,
            "Pas encore inscrit?",
            status_code=200
        )
        # test if the user was created
        user = User.objects.all()
        self.assertEqual(len(user), 2)

    def test_signup_post_with_bad_information(self):
        response_post = self.client.post(reverse("signup"), {
                "email": "bademail",
                "password1": self.password,
                "password2": self.password
            },
            follow=True
        )
        self.assertContains(
            response_post,
            "Saisissez une adresse de courriel valide.",
            status_code=200
        )

    def test_signup_post_with_an_existing_email(self):
        response_post = self.client.post(reverse("signup"), {
                "email": self.username,
                "password1": self.password,
                "password2": self.password
            },
            follow=True
        )
        self.assertContains(
            response_post,
            "Un objet Utilisateur avec ce champ Email existe déjà.",
            status_code=200
        )

    def test_login_class_view(self):
        response_get = self.client.get(reverse("login"))
        self.assertContains(
            response_get,
            "Pas encore inscrit?",
            status_code=200
        )

    def test_login_with_good_information(self):
        response_post = self.client.post(reverse("login"), {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(response_post.status_code, 200)

    def test_login_with_bad_information(self):
        response_post = self.client.post(reverse("login"), {
                "username": self.username2,
                "password": "badpassword"
            }
        )
        self.assertContains(
            response_post,
            "Votre nom d'utilisateur ou votre mot de passe est incorrect. Veuillez réessayer",
            status_code=200
        )

    def test_profile_view_redirect_if_not_logged_in(self):
        response_get = self.client.get(reverse("profile"))
        self.assertEqual(response_get.status_code, 302)
        self.assertRedirects(response_get, "/accounts/login/?next=/accounts/profile/")

    def test_logout(self):
        self.client.login(email=self.username, password=self.password)
        response_logout = self.client.get(reverse("logout"), follow=True)
        self.assertContains(
            response_logout,
            "Du gras, oui, mais de qualité!",
            status_code=200
        )

    def test_profile(self):
        # user not logged in
        request = self.factory.get('profile')
        request.user = AnonymousUser()
        response = Profile.as_view()(request)
        self.assertEqual(response.status_code, 302)

        # user logged in
        request.user = self.user
        response = Profile.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'usernametest')

    def test_profile_get_context(self):
        request = self.factory.get('profile')
        request.user = self.user
        view = Profile()
        view.setup(request)
        context = view.get_context_data()
        self.assertEqual(context['username'], 'Usernametest')
        self.assertEqual(context['email'], self.user)
        self.assertEqual(context['avatar'], 0)

    def test_extract_username_from_mail(self):
        request = self.factory.get('profile')
        request.user = self.username
        result = Profile.extract_username_from_mail(request.user)
        self.assertEqual(result, 'usernametest')

    def test_imageprofileform(self):
        form = ImageProfileForm(data={}, files={"img_profile": self.image})
        self.assertTrue(form.is_valid())

    def delete_photo_file(self):
        os.remove("media/avatar/test.png")

    def test_post_imagefield(self):
        # post with image
        request = self.factory.post('profile', {'img_profile': self.image})
        request.user = self.user
        response = Profile().post(request)
        self.assertEqual(response.status_code, 302)
        # post
        request2 = self.factory.post('profile')
        response2 = Profile().post(request2)
        self.assertEqual(response2.status_code, 200)

        # get context_data with a new image profile
        request = self.factory.get('profile')
        request.user = self.user
        view = Profile()
        view.setup(request)
        context = view.get_context_data()
        avatar_profile = ImageProfile.objects.get(user_id=self.user)
        self.assertEqual(avatar_profile.img_profile, "avatar/test.png")
        self.assertEqual(context['avatar'], avatar_profile)
        self.delete_photo_file()
