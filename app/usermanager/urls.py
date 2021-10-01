from usermanager.views import Signup, Login, Logout, Profile
from django.urls import path


urlpatterns = [
    path('accounts/signup/', Signup.as_view(), name="signup"),
    path('accounts/login/', Login.as_view(), name="login"),
    path('accounts/profile/', Profile.as_view(), name="profile"),
    path('accounts/logout/', Logout.as_view(), name="logout"),
]
