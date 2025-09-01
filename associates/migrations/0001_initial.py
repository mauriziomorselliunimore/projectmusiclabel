from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Associate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, default='2025-09-01')),
                ('specialization', models.CharField(help_text='Specializzazione principale', max_length=100)),
                ('skills', models.CharField(help_text='Competenze separate da virgola', max_length=300)),
                ('experience_level', models.CharField(choices=[('beginner', 'Principiante'), ('intermediate', 'Intermedio'), ('advanced', 'Avanzato'), ('professional', 'Professionale')], default='intermediate', max_length=20)),
                ('years_experience', models.PositiveIntegerField(blank=True, help_text='Anni di esperienza', null=True)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Tariffa oraria in €', max_digits=6, null=True)),
                ('availability', models.CharField(blank=True, help_text='Disponibilità oraria', max_length=200)),
                ('is_available', models.BooleanField(default=True, help_text='Disponibile per nuovi progetti')),
                ('bio', models.TextField(blank=True, help_text='Biografia professionale', max_length=1000)),
                ('portfolio_description', models.TextField(blank=True, help_text='Descrizione del portfolio', max_length=500)),
                ('location', models.CharField(blank=True, help_text='Città, Provincia', max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('website', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, default='2025-09-01')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('completion_date', models.DateField(null=True, blank=True)),
                ('external_image_url', models.URLField(blank=True, help_text='Link a immagine (Imgur, Google Drive, etc.)')),
                ('external_audio_url', models.URLField(blank=True, help_text='Link audio (SoundCloud, YouTube, etc.)')),
                ('external_url', models.URLField(blank=True, help_text='Link esterno principale (YouTube, SoundCloud, sito web, etc.)')),
                ('associate', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='portfolio_items', to='associates.associate')),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Lunedì'), (1, 'Martedì'), (2, 'Mercoledì'), (3, 'Giovedì'), (4, 'Venerdì'), (5, 'Sabato'), (6, 'Domenica')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=200)),
                ('associate', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='availability_slots', to='associates.associate')),
            ],
            options={
                'verbose_name_plural': 'Availabilities',
                'ordering': ['day_of_week', 'start_time'],
                'db_table': 'associates_availability',
                'unique_together': {('associate', 'day_of_week', 'start_time', 'end_time')},
            },
        ),
    ]
