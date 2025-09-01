from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
        ('associates', '0002_add_profile_fields'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together=set(),  # Rimuove tutti i vincoli unique_together esistenti
        ),
        migrations.RemoveField(
            model_name='availability',
            name='day_of_week',
        ),
        migrations.AddField(
            model_name='availability',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='availability',
            name='is_recurring',
            field=models.BooleanField(default=False, help_text='Se true, questa disponibilità si ripete ogni settimana'),
        ),
        migrations.AddField(
            model_name='availability',
            name='recurrence_end_date',
            field=models.DateField(blank=True, null=True, help_text='Data fine ricorrenza'),
        ),
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together={('associate', 'date', 'start_time', 'end_time')},
        ),
    ]
