"""
Django command to make migrations for CollaborationProposal model.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('messaging', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollaborationProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('production', 'Produzione Musicale'), ('recording', 'Sessioni Registrazione'), ('mixing', 'Mixing & Mastering'), ('live', 'Performance Live'), ('songwriting', 'Songwriting'), ('other', 'Altro')], max_length=20)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', models.TextField()),
                ('timeline', models.CharField(choices=[('asap', 'Il prima possibile'), ('week', 'Entro una settimana'), ('month', 'Entro un mese'), ('flexible', 'Flessibile')], max_length=20)),
                ('mode', models.CharField(choices=[('remote', 'Lavoro remoto'), ('studio', 'In studio'), ('hybrid', 'Misto (remoto + studio)'), ('flexible', 'Da definire')], max_length=20)),
                ('reference_links', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'In attesa'), ('accepted', 'Accettata'), ('rejected', 'Rifiutata'), ('counter', 'Controproposta')], default='pending', max_length=20)),
                ('response_message', models.TextField(blank=True, null=True)),
                ('counter_budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('counter_notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('original_message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposals', to='messaging.message')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_proposals', to='auth.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
