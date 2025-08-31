from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_message_date', models.DateTimeField(blank=True, null=True)),
                ('participant_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_participant_1', to=settings.AUTH_USER_MODEL)),
                ('participant_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_participant_2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
                'unique_together': {('participant_1', 'participant_2')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
                ('message_type', models.CharField(choices=[('general', 'Messaggio Generale'), ('booking_request', 'Richiesta Prenotazione'), ('collaboration', 'Proposta Collaborazione'), ('inquiry', 'Richiesta Informazioni'), ('quote_request', 'Richiesta Preventivo'), ('other', 'Altro')], default='general', max_length=20)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messaging.conversation')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='conversation',
            name='last_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='messaging.message'),
        ),
    ]
