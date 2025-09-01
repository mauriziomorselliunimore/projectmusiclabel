from django.db import migrations, models
import django.db.models.deletion

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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
