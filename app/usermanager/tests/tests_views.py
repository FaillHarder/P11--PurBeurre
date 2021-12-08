from usermanager.views import Profile
from usermanager.models import User, ImageProfile

from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from django.urls import reverse
from django.test import TestCase
# from PIL import Image


# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = "usernametest@test.fr"
        self.password = "passwordtest"
        self.username2 = "usernametest2@test.fr"
        User.objects.create(
            email=self.username,
            password=self.password
        )
        self.user = User.objects.get(email=self.username)
        self.fake_image = SimpleUploadedFile("avatartest.png", b"file_content", content_type='image/png')
        # ImageProfile.objects.create(user=self.user, img_profile=self.fake_image)
        return super().setUp()

    def test_signup(self):
        response_get = self.client.get(reverse("signup"))
        self.assertContains(response_get, "Créer un compte", status_code=200)

        # test form post with good information and display login.html
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

        # test that we cannot register the same email
        response_post = self.client.post(reverse("signup"), {
                "email": self.username2,
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

    def test_login(self):
        response_get = self.client.get(reverse("login"))
        self.assertContains(
            response_get,
            "Pas encore inscrit?",
            status_code=200
        )

        # test user login with good credentials
        response_post = self.client.post(reverse("login"), {
                "username": self.username2,
                "password": self.password
            }
        )
        self.assertContains(
            response_post,
            "Pas encore inscrit?",
            status_code=200
        )

        # test user login with bad credentials
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
        # the user has the default avatar
        self.assertContains(response, 0)

    def test_profile_post(self):

        pass
        

    def test_extract_username_from_mail(self):
        request = self.factory.get('profile')
        request.user = self.username
        result = Profile.extract_username_from_mail(request.user)
        self.assertEqual(result, 'usernametest')
    
    def test_try_if_user_img_exist_delete_or_create(self):
        pass