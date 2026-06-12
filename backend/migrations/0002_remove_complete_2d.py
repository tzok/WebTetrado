from django.db import migrations


def drop_complete_2d(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(
        'ALTER TABLE "backend_tetradorequest" '
        'DROP COLUMN IF EXISTS "complete_2d";'
    )


def add_complete_2d(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(
        'ALTER TABLE "backend_tetradorequest" '
        'ADD COLUMN "complete_2d" boolean NOT NULL DEFAULT false;'
    )


class Migration(migrations.Migration):
    dependencies = [("backend", "0001_initial")]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(drop_complete_2d, add_complete_2d)
            ],
            state_operations=[],
        )
    ]
