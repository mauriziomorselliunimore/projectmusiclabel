from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=lambda apps, schema_editor: print(
                [f.column for f in schema_editor.connection.introspection.get_table_description(
                    schema_editor.connection.cursor(),
                    "artists_artist"
                )]
            ),
            reverse_code=lambda apps, schema_editor: None
        ),
    ]
