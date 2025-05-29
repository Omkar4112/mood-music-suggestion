from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address must be unique.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Try to find user by email if username lookup fails
        user_queryset = User.objects.filter(username=username_or_email)
        if not user_queryset.exists():
            user_queryset = User.objects.filter(email=username_or_email)
            if user_queryset.exists():
                self.cleaned_data['username'] = user_queryset.first().username

        return super().clean()
