from django import forms
from .models import Booking
from django.utils import timezone
from datetime import timedelta

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_type', 'session_date', 'duration_hours', 'location', 'notes', 'special_requirements']
        widgets = {
            'booking_type': forms.Select(attrs={
                'class': 'form-select dark-select',
                'placeholder': 'Seleziona il tipo di sessione'
            }),
            'session_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M'),
                'max': (timezone.now() + timedelta(days=90)).strftime('%Y-%m-%dT%H:%M')
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '8',
                'step': '0.5'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome dello studio o indirizzo'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dettagli sulla sessione (es. brani da registrare, strumenti necessari, etc.)'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Eventuali richieste particolari'
            })
        }
        labels = {
            'booking_type': 'Tipo di Sessione',
            'session_date': 'Data e Ora',
            'duration_hours': 'Durata (ore)',
            'location': 'Location',
            'notes': 'Note',
            'special_requirements': 'Richieste Speciali'
        }
        help_texts = {
            'booking_type': 'Seleziona il tipo di sessione che vuoi prenotare',
            'session_date': 'Scegli data e ora di inizio della sessione',
            'duration_hours': 'Indica la durata prevista in ore (min 1, max 8)',
            'location': 'Specifica dove si svolgerà la sessione',
            'notes': 'Aggiungi dettagli sulla sessione',
            'special_requirements': 'Indica eventuali necessità particolari'
        }

    def __init__(self, *args, **kwargs):
        associate = kwargs.pop('associate', None)
        super().__init__(*args, **kwargs)
        
        # Personalizza le opzioni del booking_type in base alla specializzazione dell'associato
        if associate:
            available_types = []
            if 'producer' in associate.specialization.lower():
                available_types.extend(['recording', 'production'])
            if 'mixing' in associate.specialization.lower():
                available_types.append('mixing')
            if 'mastering' in associate.specialization.lower():
                available_types.append('mastering')
            if 'teach' in associate.specialization.lower():
                available_types.append('lesson')
            
            if available_types:
                choices = [choice for choice in self.fields['booking_type'].choices 
                          if choice[0] in available_types]
                self.fields['booking_type'].choices = choices

    def clean_session_date(self):
        session_date = self.cleaned_data.get('session_date')
        if session_date:
            # Verifica che la data non sia nel passato
            if session_date < timezone.now():
                raise forms.ValidationError("Non puoi prenotare una sessione nel passato!")
            
            # Verifica che la data non sia troppo nel futuro
            max_future = timezone.now() + timedelta(days=90)
            if session_date > max_future:
                raise forms.ValidationError("Non puoi prenotare oltre 90 giorni in anticipo!")
            
            # Verifica l'orario (es. solo tra le 9 e le 22)
            if session_date.hour < 9 or session_date.hour >= 22:
                raise forms.ValidationError("Le sessioni sono disponibili solo tra le 9:00 e le 22:00!")
        
        return session_date

    def clean_duration_hours(self):
        duration = self.cleaned_data.get('duration_hours')
        if duration:
            if duration < 1:
                raise forms.ValidationError("La durata minima è di 1 ora!")
            if duration > 8:
                raise forms.ValidationError("La durata massima è di 8 ore!")
        return duration
