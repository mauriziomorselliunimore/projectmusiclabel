from django import forms
from .models import QuoteRequest

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrivi la richiesta di preventivo...'
            })
        }
        labels = {
            'message': 'Messaggio per l’associato'
        }
        help_texts = {
            'message': 'Spiega cosa ti serve, il tipo di lavoro, le tempistiche, ecc.'
        }
from django import forms
from .models import Booking, Availability
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
            'session_date': 'Scegli la data e l\'ora di inizio della sessione',
            'duration_hours': 'Indica la durata prevista in ore',
            'location': 'Specifica dove si terrà la sessione',
            'notes': 'Aggiungi dettagli importanti sulla sessione',
            'special_requirements': 'Indica eventuali necessità particolari'
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['is_recurring', 'day_of_week', 'specific_date', 'start_time', 'end_time']
        widgets = {
            'specific_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'is_recurring': 'Disponibilità Ricorrente',
            'day_of_week': 'Giorno della Settimana',
            'specific_date': 'Data Specifica',
            'start_time': 'Ora Inizio',
            'end_time': 'Ora Fine'
        }
        help_texts = {
            'is_recurring': 'Seleziona se questa disponibilità si ripete ogni settimana',
            'day_of_week': 'Per disponibilità ricorrenti, seleziona il giorno della settimana',
            'specific_date': 'Per disponibilità una tantum, seleziona la data specifica',
            'start_time': 'Ora di inizio della disponibilità',
            'end_time': 'Ora di fine della disponibilità',
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
