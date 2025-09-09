from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_add_profile_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='profile_icon',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='profile_icon_color',
        ),
    ]
