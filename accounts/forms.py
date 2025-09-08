from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models.profile import Profile

class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = [
        ('artist', 'Artista'),
        ('associate', 'Associato'),
    ]
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'esempio@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cognome'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizza i widget dei campi password
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Conferma password'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Questa email è già registrata.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("L'username deve essere di almeno 3 caratteri.")
        if not username.isalnum():
            raise forms.ValidationError("L'username può contenere solo lettere e numeri.")
        return username
    
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
        fields = ['phone', 'location', 'bio', 'external_avatar_url', 'profile_icon', 'profile_icon_color']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Racconta qualcosa di te...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+39 123 456 7890',
                'pattern': '\\+[0-9]{2,3}\\s?[0-9]{6,14}',
                'title': 'Inserisci un numero di telefono valido (es: +39 123 456 7890)'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Roma, Italia'
            }),
            'external_avatar_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://imgur.com/abc123.jpg (opzionale)'
            }),
            'profile_icon': forms.RadioSelect(attrs={
                'class': 'icon-choice-input'
            }),
            'profile_icon_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'title': 'Scegli il colore per la tua icona'
            })
        }
        labels = {
            'phone': 'Telefono',
            'location': 'Località',
            'bio': 'Biografia',
            'external_avatar_url': 'URL Avatar Esterno',
            'profile_icon': 'Icona Profilo',
            'profile_icon_color': 'Colore Icona'
        }
        help_texts = {
            'phone': 'Inserisci il tuo numero di telefono nel formato internazionale',
            'location': 'La tua città o regione',
            'bio': 'Una breve descrizione di te o della tua attività',
            'external_avatar_url': 'URL di una tua immagine profilo da un servizio esterno',
            'profile_icon': 'Scegli un\'icona per rappresentare il tuo profilo',
            'profile_icon_color': 'Scegli un colore per la tua icona'
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Rimuovi spazi e caratteri non necessari
            phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            # Verifica formato internazionale
            if not phone.startswith('+'):
                raise forms.ValidationError("Il numero deve iniziare con il prefisso internazionale (+)")
            if len(phone) < 10 or len(phone) > 15:
                raise forms.ValidationError("Il numero di telefono non sembra valido")
        return phone

    def clean_external_avatar_url(self):
        url = self.cleaned_data.get('external_avatar_url')
        if url:
            if not url.startswith(('http://', 'https://')):
                raise forms.ValidationError("L'URL deve iniziare con http:// o https://")
            # Verifica che sia un'immagine
            if not any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                raise forms.ValidationError("L'URL deve puntare a un'immagine (jpg, jpeg, png, gif)")
        return url

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['external_avatar_url'].help_text = 'Link a foto profilo online (Imgur, Google Drive, etc.). Se vuoto, verrà usato Gravatar.'