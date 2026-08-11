from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile


# ==========================================================
#                   REGISTER FORM
# ==========================================================

class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = [

            "username",

            "email",

            "password1",

            "password2",

        ]

    # ------------------------------------------------------
    # Validate Email
    # ------------------------------------------------------

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(

            email__iexact=email

        ).exists():

            raise forms.ValidationError(

                "An account with this email already exists."

            )

        return email


# ==========================================================
#               USER UPDATE FORM
# ==========================================================

class UserUpdateForm(ModelForm):

    class Meta:

        model = User

        fields = [

            "first_name",

            "last_name",

            "email",

        ]

    # ------------------------------------------------------
    # Validate Email
    # ------------------------------------------------------

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(

            email__iexact=email

        ).exclude(

            id=self.instance.id

        ).exists():

            raise forms.ValidationError(

                "This email is already in use."

            )

        return email


# ==========================================================
#              PROFILE UPDATE FORM
# ==========================================================

class ProfileUpdateForm(ModelForm):

    class Meta:

        model = Profile

        fields = [

            "image",

        ]