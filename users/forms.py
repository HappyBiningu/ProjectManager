from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True)
    surname = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Enter your password"}),
        required=True
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Confirm your password"}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
     

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None  
        self.fields['username'].label = "Enter Username"
        self.fields['email'].widget.attrs['placeholder'] = "Enter your email address"

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                name=self.cleaned_data['name'],
                surname=self.cleaned_data['surname']
            )
        return user