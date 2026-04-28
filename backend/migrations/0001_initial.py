# Generated manually for backend app initial migration

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Metadata",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("onz_class", models.CharField(blank=True, max_length=100)),
                ("tetrad_combination", models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Nucleotide",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("query_id", models.IntegerField()),
                ("number", models.IntegerField()),
                ("symbol", models.CharField(max_length=20)),
                ("chain", models.CharField(max_length=20)),
                ("glycosidicBond", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=100)),
                ("chi_angle", models.CharField(max_length=20)),
                ("molecule", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="TemporaryFile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/")),
                ("file_extension", models.CharField(max_length=20)),
                ("timestamp", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PushInformation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hash_id", models.UUIDField(default=uuid.uuid1, editable=False)),
                ("browser", models.CharField(max_length=100)),
                ("user_agent", models.CharField(blank=True, max_length=500)),
                ("endpoint", models.URLField(max_length=500)),
                ("auth", models.CharField(max_length=100)),
                ("p256dh", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="BasePair",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("edge3", models.CharField(max_length=50)),
                ("edge5", models.CharField(max_length=50)),
                ("stericity", models.CharField(max_length=50)),
                ("lw", models.CharField(default="", max_length=3)),
                ("inTetrad", models.BooleanField(default=False)),
                ("canonical", models.BooleanField(default=False)),
                (
                    "nt1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="nucleotide_bp_1",
                        to="backend.nucleotide",
                    ),
                ),
                (
                    "nt2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="nucleotide_bp_2",
                        to="backend.nucleotide",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tetrad",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("query_id", models.IntegerField()),
                ("planarity", models.FloatField(default=0)),
                (
                    "tetrad_file",
                    models.FileField(blank=True, upload_to="files/results/tetrad/"),
                ),
                (
                    "metadata",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.metadata",
                    ),
                ),
                (
                    "nt1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="nucleotide1",
                        to="backend.nucleotide",
                    ),
                ),
                (
                    "nt2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="nucleotide2",
                        to="backend.nucleotide",
                    ),
                ),
                (
                    "nt3",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="nucleotide3",
                        to="backend.nucleotide",
                    ),
                ),
                (
                    "nt4",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="nucleotide4",
                        to="backend.nucleotide",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TetradPair",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rise", models.FloatField()),
                ("twist", models.FloatField()),
                ("strand_direction", models.CharField(max_length=100)),
                (
                    "tetrad1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="tetrad1",
                        to="backend.tetrad",
                    ),
                ),
                (
                    "tetrad2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="tetrad2",
                        to="backend.tetrad",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Loop",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("length", models.IntegerField()),
                ("type", models.CharField(max_length=50)),
                ("nucleotide", models.ManyToManyField(to="backend.nucleotide")),
            ],
        ),
        migrations.CreateModel(
            name="Quadruplex",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("UNI", "unimolecular"),
                            ("BI", "bimolecular"),
                            ("TETRA", "tetramolecular"),
                            ("OTHER", "other"),
                        ],
                        default="OTHER",
                        max_length=10,
                    ),
                ),
                ("molecule", models.CharField(blank=True, max_length=100)),
                ("loop_classification", models.CharField(blank=True, max_length=50)),
                (
                    "metadata",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.metadata",
                    ),
                ),
                ("loop", models.ManyToManyField(to="backend.loop")),
                ("tetrad", models.ManyToManyField(to="backend.tetrad")),
            ],
        ),
        migrations.CreateModel(
            name="Helice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quadruplex", models.ManyToManyField(to="backend.quadruplex")),
                ("tetrad_pair", models.ManyToManyField(to="backend.tetradpair")),
            ],
        ),
        migrations.CreateModel(
            name="TetradoRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hash_id", models.UUIDField(default=uuid.uuid1, editable=False)),
                ("source", models.IntegerField(choices=[(1, "RCSB"), (2, "File")])),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "REQUESTED"),
                            (2, "QUEUED"),
                            (3, "PROCESSING"),
                            (4, "DONE"),
                            (5, "ERROR"),
                        ]
                    ),
                ),
                (
                    "structure_body",
                    models.FileField(blank=True, upload_to="files/structures/"),
                ),
                (
                    "structure_body_original",
                    models.FileField(
                        blank=True, upload_to="files/structures_original/"
                    ),
                ),
                ("file_extension", models.CharField(max_length=20)),
                ("dot_bracket_line1", models.TextField(blank=True)),
                ("dot_bracket_line2", models.TextField(blank=True)),
                ("dot_bracket_sequence", models.TextField(blank=True)),
                ("no_reorder", models.BooleanField()),
                ("g4_limited", models.BooleanField()),
                ("model", models.IntegerField(default=1)),
                ("analyzer", models.CharField(default="INTERNAL", max_length=50)),
                ("name", models.CharField(blank=True, max_length=200)),
                ("structure_method", models.CharField(blank=True, max_length=200)),
                ("idcode", models.CharField(blank=True, max_length=20)),
                ("timestamp", models.DateTimeField(auto_now=True)),
                ("elTetradoKey", models.CharField(max_length=100)),
                ("cached_result", models.TextField(blank=True)),
                ("error", models.TextField(blank=True, default="")),
                (
                    "r_chie",
                    models.FileField(blank=True, upload_to="files/results/r_chie/"),
                ),
                (
                    "r_chie_canonical",
                    models.FileField(
                        blank=True, upload_to="files/results/r_chie-canonical/"
                    ),
                ),
                (
                    "varna",
                    models.FileField(blank=True, upload_to="files/results/varna/"),
                ),
                (
                    "varna_can",
                    models.FileField(blank=True, upload_to="files/results/varna-can/"),
                ),
                (
                    "varna_non_can",
                    models.FileField(
                        blank=True, upload_to="files/results/varna-non-can/"
                    ),
                ),
                (
                    "varna_can_non_can",
                    models.FileField(
                        blank=True, upload_to="files/results/varna-can_non-can/"
                    ),
                ),
                (
                    "draw_tetrado",
                    models.FileField(blank=True, upload_to="files/results/layers/"),
                ),
                (
                    "base_pair",
                    models.ManyToManyField(blank=True, to="backend.basepair"),
                ),
                ("helice", models.ManyToManyField(blank=True, to="backend.helice")),
                (
                    "push_notification",
                    models.ManyToManyField(blank=True, to="backend.pushinformation"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=255)),
                ("info", models.CharField(max_length=255)),
                ("traceback", models.TextField(default="")),
                ("timestamp", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "webtetrado_logs",
                "verbose_name_plural": "Error logs",
            },
        ),
    ]
