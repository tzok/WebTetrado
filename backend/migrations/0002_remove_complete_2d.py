from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("backend", "0001_initial")]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        'ALTER TABLE "backend_tetradorequest" '
                        'DROP COLUMN IF EXISTS "complete_2d";'
                    ),
                    reverse_sql=(
                        'ALTER TABLE "backend_tetradorequest" '
                        'ADD COLUMN "complete_2d" boolean NOT NULL DEFAULT false;'
                    ),
                )
            ],
            state_operations=[],
        )
    ]
