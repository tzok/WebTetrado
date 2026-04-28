from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0003_basepair_lw"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nucleotide",
            name="chain",
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
