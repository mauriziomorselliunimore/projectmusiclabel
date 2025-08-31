from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
                ('message_type', models.CharField(choices=[('general', 'Messaggio Generale'), ('booking_request', 'Richiesta Prenotazione'), ('collaboration', 'Proposta Collaborazione'), ('inquiry', 'Richiesta Informazioni'), ('quote_request', 'Richiesta Preventivo'), ('other', 'Altro')], default='general', max_length=20)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_message_date', models.DateTimeField(blank=True, null=True)),
                ('participant_1', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='conversations_as_participant_1', to='auth.user')),
                ('participant_2', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='conversations_as_participant_2', to='auth.user')),
            ],
            options={
                'ordering': ['-updated_at'],
                'unique_together': {('participant_1', 'participant_2')},
            },
        ),
        migrations.AddField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='messages', to='messaging.conversation'),
        ),
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='received_messages', to='auth.user'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='sent_messages', to='auth.user'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='last_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='+', to='messaging.message'),
        ),
    ]
