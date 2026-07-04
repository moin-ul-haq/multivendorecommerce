from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "input_box"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input_box"}))


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input_box"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input_box"})
    )
    role = forms.ChoiceField(
        choices=[("customer", "Customer"), ("owner", "Owner")],
        widget=forms.Select(attrs={"class": "input_box"}),
    )

    class Meta:
        model = User
        fields = ["username", "name", "age", "email", "address", "role"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input_box"}),
            "name": forms.TextInput(attrs={"class": "input_box"}),
            "age": forms.NumberInput(attrs={"class": "input_box"}),
            "email": forms.EmailInput(attrs={"class": "input_box"}),
            "address": forms.Textarea(attrs={"class": "input_box", "rows": 4}),
            "role": forms.Select(attrs={"class": "input_box"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
