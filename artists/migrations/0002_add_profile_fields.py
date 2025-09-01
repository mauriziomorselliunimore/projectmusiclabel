from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='profile_icon',
            field=models.CharField(blank=True, choices=[('bi-person-circle', 'Persona'), ('bi-music-note', 'Nota Musicale'), ('bi-mic', 'Microfono'), ('bi-vinyl', 'Vinile'), ('bi-headphones', 'Cuffie'), ('bi-speaker', 'Speaker'), ('bi-soundwave', 'Onda Sonora'), ('bi-boombox', 'Boombox'), ('bi-stars', 'Stelle'), ('bi-lightning', 'Fulmine')], default='bi-person-circle', help_text='Icona del profilo', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='profile_icon_color',
            field=models.CharField(blank=True, default='#ff2e88', help_text="Colore dell'icona (es. #ff2e88)", max_length=7, null=True),
        ),
    ]
