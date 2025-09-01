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
                ('specialization', models.CharField(help_text='Specializzazione principale', max_length=100)),
                ('skills', models.CharField(help_text='Competenze separate da virgola', max_length=300)),
                ('experience_level', models.CharField(choices=[('beginner', 'Principiante'), ('intermediate', 'Intermedio'), ('advanced', 'Avanzato'), ('professional', 'Professionale')], default='intermediate', max_length=20)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Tariffa oraria in €', max_digits=6, null=True)),
                ('availability', models.CharField(blank=True, help_text='Disponibilità oraria', max_length=200)),
                ('user', models.OneToOneField(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('project_type', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('link', models.URLField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='portfolio/')),
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
                ('associate', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='availability_slots', to='associates.associate')),
            ],
        ),
    ]
