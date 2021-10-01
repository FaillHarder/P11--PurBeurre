from usermanager.models import User

from django.urls import reverse
from django.test import TestCase


# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        self.username = "usernametest@test.fr"
        self.password = "passwordtest"
        return super().setUp()

    def test_signup(self):
        response_get = self.client.get(reverse("signup"))
        self.assertContains(response_get, "Créer un compte", status_code=200)

        # test form post with good information and display login.html
        response_post = self.client.post(reverse("signup"), {
                "email": self.username,
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
        self.assertEqual(len(user), 1)

        # test that we cannot register the same email
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

    def test_login(self):
        response_get = self.client.get(reverse("login"))
        self.assertContains(
            response_get,
            "Pas encore inscrit?",
            status_code=200
        )

        # test user login with good credentials
        response_post = self.client.post(reverse("login"), {
                "username": self.username,
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
                "username": self.username,
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
