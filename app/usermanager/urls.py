from usermanager import views
from usermanager.views import Signup, Login, Logout, Profile
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/signup/', Signup.as_view(), name="signup"),
    path('accounts/login/', Login.as_view(), name="login"),
    path('accounts/profile/', Profile.as_view(), name="profile"),
    path('accounts/logout/', Logout.as_view(), name="logout"),
    path('accounts/profile/customize', views.customize, name="customize"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
