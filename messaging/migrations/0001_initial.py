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
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('message_type', models.CharField(choices=[('general', 'Messaggio Generale'), ('booking_request', 'Richiesta Prenotazione'), ('collaboration', 'Proposta Collaborazione'), ('inquiry', 'Richiesta Informazioni'), ('quote_request', 'Richiesta Preventivo'), ('other', 'Altro')], default='general', max_length=20)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messaging.conversation')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('message', 'New Message'), ('proposal', 'New Proposal'), ('proposal_update', 'Proposal Update'), ('counter_proposal', 'Counter Proposal'), ('follow', 'New Follower')], max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('action_url', models.CharField(blank=True, max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('related_message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='messaging.message')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
