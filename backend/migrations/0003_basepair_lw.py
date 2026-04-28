from django.db import migrations, models


def add_lw_field(apps, schema_editor):
    from django.db import connection

    cursor = connection.cursor()
    if connection.vendor == "postgresql":
        cursor.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'backend_basepair'"
        )
        columns = [row[0] for row in cursor.fetchall()]
    else:
        cursor.execute("PRAGMA table_info(backend_basepair)")
        columns = [row[1] for row in cursor.fetchall()]

    if "lw" not in columns:
        cursor.execute(
            "ALTER TABLE backend_basepair ADD COLUMN lw varchar(3) DEFAULT ''"
        )


class Migration(migrations.Migration):
    dependencies = [("backend", "0002_remove_complete_2d")]

    operations = [
        migrations.RunPython(add_lw_field),
    ]
