from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import FileExtensionValidator
from artists.models import validate_audio_file_size

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_name', models.CharField(help_text="Nome d'arte", max_length=100)),
                ('profile_icon', models.CharField(blank=True, choices=[('bi-person-circle', 'Persona'), ('bi-music-note', 'Nota Musicale'), ('bi-mic', 'Microfono'), ('bi-vinyl', 'Vinile'), ('bi-headphones', 'Cuffie'), ('bi-speaker', 'Speaker'), ('bi-soundwave', 'Onda Sonora'), ('bi-boombox', 'Boombox'), ('bi-stars', 'Stelle'), ('bi-lightning', 'Fulmine')], default='bi-person-circle', help_text='Icona del profilo', max_length=50, null=True)),
                ('profile_icon_color', models.CharField(blank=True, default='#ff2e88', help_text="Colore dell'icona (es. #ff2e88)", max_length=7, null=True)),
                ('genres', models.CharField(help_text='Generi musicali separati da virgola', max_length=200)),
                ('bio', models.TextField(blank=True, max_length=1000)),
                ('spotify_url', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('soundcloud_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
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
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demos', to='artists.artist')),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
