from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = [
        ('artist', 'Artista'),
        ('associate', 'Associato'),
    ]
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'location', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'phone': forms.TextInput(attrs={'placeholder': '+39 123 456 7890'}),
            'location': forms.TextInput(attrs={'placeholder': 'Roma, Italia'}),
        }