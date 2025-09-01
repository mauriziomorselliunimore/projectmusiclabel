from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_welcome_message',
            field=models.BooleanField(default=False, help_text='Indica se questo è un messaggio di benvenuto automatico'),
        ),
    ]
