from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model


class SignUpForm(auth_forms.UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta(auth_forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email',)
