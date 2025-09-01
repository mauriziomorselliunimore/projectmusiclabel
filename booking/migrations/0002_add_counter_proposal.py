from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='counter_proposal_date',
            field=models.DateTimeField(null=True, blank=True, help_text='Data proposta alternativa'),
        ),
        migrations.AddField(
            model_name='booking',
            name='counter_proposal_duration',
            field=models.PositiveIntegerField(null=True, blank=True, help_text='Durata proposta alternativa in ore'),
        ),
        migrations.AddField(
            model_name='booking',
            name='counter_proposal_notes',
            field=models.TextField(blank=True, help_text='Note sulla proposta alternativa'),
        ),
        migrations.AddField(
            model_name='booking',
            name='is_counter_proposal',
            field=models.BooleanField(default=False, help_text='Indica se questa è una controproposta'),
        ),
        migrations.AddField(
            model_name='booking',
            name='counter_proposal_status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('pending', 'In Attesa'),
                    ('accepted', 'Accettata'),
                    ('rejected', 'Rifiutata')
                ],
                null=True,
                blank=True,
                help_text='Stato della controproposta'
            ),
        ),
    ]
