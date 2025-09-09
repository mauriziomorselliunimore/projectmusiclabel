from django.db import migrations, models
import django.db.models.deletion
from datetime import timedelta

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_type', models.CharField(max_length=20)),
                ('session_date', models.DateTimeField()),
                ('duration_hours', models.PositiveIntegerField(default=2)),
                ('location', models.CharField(max_length=200, blank=True)),
                ('notes', models.TextField(max_length=1000, blank=True)),
                ('special_requirements', models.TextField(max_length=500, blank=True)),
                ('status', models.CharField(max_length=20)),
                ('total_cost', models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artists.artist')),
                ('associate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='associates.associate')),
            ],
            options={
                'ordering': ['-session_date'],
            },
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(null=True, blank=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_recurring', models.BooleanField(default=True)),
                ('specific_date', models.DateField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('associate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='associates.associate')),
            ],
            options={
                'ordering': ['day_of_week', 'start_time'],
            },
        ),
    ]
