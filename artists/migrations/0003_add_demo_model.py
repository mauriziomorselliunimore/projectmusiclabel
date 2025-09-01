from django.db import migrations, models
from django.core.validators import FileExtensionValidator
from artists.models import validate_audio_file_size

class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0002_add_profile_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('external_audio_url', models.URLField(blank=True, help_text='Link a SoundCloud, YouTube, Spotify, etc.')),
                ('audio_file', models.FileField(blank=True, help_text='File audio (max 10MB, formati: MP3, WAV)', null=True, upload_to='audio_files/%Y/%m/%d/', validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav']), validate_audio_file_size])),
                ('genre', models.CharField(choices=[('rock', 'Rock'), ('pop', 'Pop'), ('hip-hop', 'Hip-Hop'), ('electronic', 'Electronic'), ('jazz', 'Jazz'), ('blues', 'Blues'), ('country', 'Country'), ('reggae', 'Reggae'), ('folk', 'Folk'), ('classical', 'Classical'), ('r&b', 'R&B'), ('indie', 'Indie'), ('punk', 'Punk'), ('metal', 'Metal'), ('funk', 'Funk'), ('other', 'Altro')], max_length=50)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('duration', models.CharField(blank=True, help_text='mm:ss', max_length=10)),
                ('waveform_data', models.JSONField(blank=True, help_text="Dati per la visualizzazione della forma d'onda", null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('is_public', models.BooleanField(default=True)),
                ('artist', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='demos', to='artists.artist')),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
