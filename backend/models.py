import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class Metadata(models.Model):
    onz_class = models.CharField(max_length=100, blank=True)
    tetrad_combination = models.CharField(max_length=100, blank=True)


class Nucleotide(models.Model):
    id = models.AutoField(primary_key=True)
    query_id = models.IntegerField()
    number = models.IntegerField()
    symbol = models.CharField(max_length=20)
    chain = models.CharField(max_length=20, null=True, blank=True)
    glycosidicBond = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    chi_angle = models.CharField(max_length=20)
    molecule = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class BasePair(models.Model):
    id = models.AutoField(primary_key=True)
    edge3 = models.CharField(max_length=50)
    edge5 = models.CharField(max_length=50)
    nt1 = models.ForeignKey(
        to=Nucleotide, related_name="nucleotide_bp_1", on_delete=models.DO_NOTHING
    )
    nt2 = models.ForeignKey(
        to=Nucleotide, related_name="nucleotide_bp_2", on_delete=models.DO_NOTHING
    )
    stericity = models.CharField(max_length=50)
    lw = models.CharField(max_length=3, default="")
    inTetrad = models.BooleanField(default=False)
    canonical = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nt1.name) + "-" + str(self.nt2.name)


class Tetrad(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    query_id = models.IntegerField()
    metadata = models.ForeignKey(to=Metadata, on_delete=models.CASCADE)
    planarity = models.FloatField(default=0)
    nt1 = models.ForeignKey(
        to=Nucleotide, related_name="nucleotide1", on_delete=models.DO_NOTHING
    )
    nt2 = models.ForeignKey(
        to=Nucleotide, related_name="nucleotide2", on_delete=models.DO_NOTHING
    )
    nt3 = models.ForeignKey(
        to=Nucleotide, related_name="nucleotide3", on_delete=models.DO_NOTHING
    )
    nt4 = models.ForeignKey(
        to=Nucleotide, related_name="nucleotide4", on_delete=models.DO_NOTHING
    )
    tetrad_file = models.FileField(upload_to="files/results/tetrad/", blank=True)

    def __str__(self):
        return "(" + str(self.query_id) + ") " + self.name


@receiver(pre_delete, sender=Tetrad)
def remove_file(**kwargs):
    instance = kwargs.get("instance")
    instance.tetrad_file.delete(save=False)


class TetradPair(models.Model):
    id = models.AutoField(primary_key=True)
    tetrad1 = models.ForeignKey(
        to=Tetrad, related_name="tetrad1", on_delete=models.DO_NOTHING
    )
    tetrad2 = models.ForeignKey(
        to=Tetrad, related_name="tetrad2", on_delete=models.DO_NOTHING
    )
    rise = models.FloatField()
    twist = models.FloatField()
    strand_direction = models.CharField(max_length=100)

    def __str__(self):
        return str(self.tetrad1.name) + "-" + str(self.tetrad2.name)


class Loop(models.Model):
    id = models.AutoField(primary_key=True)
    length = models.IntegerField()
    type = models.CharField(max_length=50)
    nucleotide = models.ManyToManyField(Nucleotide)

    def __str__(self):
        return (
            str(self.id)
            + ": "
            + str(self.length)
            + " "
            + "-".join([n.name for n in self.nucleotide.all()])
        )


class Quadruplex(models.Model):
    COLOR_CHOICES = (
        ("UNI", "unimolecular"),
        ("BI", "bimolecular"),
        ("TETRA", "tetramolecular"),
        ("OTHER", "other"),
    )

    id = models.AutoField(primary_key=True)
    metadata = models.ForeignKey(to=Metadata, on_delete=models.CASCADE)
    tetrad = models.ManyToManyField(Tetrad)
    loop = models.ManyToManyField(Loop)
    type = models.CharField(choices=COLOR_CHOICES, max_length=10, default="OTHER")
    molecule = models.CharField(max_length=100, blank=True)
    loop_classification = models.CharField(max_length=50, blank=True)


class Helice(models.Model):
    id = models.AutoField(primary_key=True)
    quadruplex = models.ManyToManyField(Quadruplex)
    tetrad_pair = models.ManyToManyField(TetradPair)

    def __str__(self):
        return "Helice " + str(self.id)


class TemporaryFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="uploads/")
    file_extension = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now=True)


@receiver(pre_delete, sender=TemporaryFile)
def remove_file(**kwargs):
    instance = kwargs.get("instance")
    instance.file.delete(save=False)


class PushInformation(models.Model):
    hash_id = models.UUIDField(default=uuid.uuid1, editable=False)
    browser = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=500, blank=True)
    endpoint = models.URLField(max_length=500)
    auth = models.CharField(max_length=100)
    p256dh = models.CharField(max_length=100)


class TetradoRequest(models.Model):
    class Sources(models.IntegerChoices):
        RCSB = 1, "RCSB"
        FILE = 2, "File"

    class Statuses(models.IntegerChoices):
        REQUESTED = 1, "REQUESTED"
        QUEUED = 2, "QUEUED"
        PROCESSING = 3, "PROCESSING"
        DONE = 4, "DONE"
        ERROR = 5, "ERROR"

    id = models.AutoField(primary_key=True)
    hash_id = models.UUIDField(default=uuid.uuid1, editable=False)

    source = models.IntegerField(choices=Sources.choices)
    status = models.IntegerField(choices=Statuses.choices)
    structure_body = models.FileField(upload_to="files/structures/", blank=True)
    structure_body_original = models.FileField(
        upload_to="files/structures_original/", blank=True
    )
    file_extension = models.CharField(max_length=20)

    dot_bracket_line1 = models.TextField(blank=True)
    dot_bracket_line2 = models.TextField(blank=True)
    dot_bracket_sequence = models.TextField(blank=True)
    no_reorder = models.BooleanField()
    g4_limited = models.BooleanField()
    model = models.IntegerField(default=1)
    analyzer = models.CharField(max_length=50, default="INTERNAL")

    name = models.CharField(max_length=200, blank=True)
    structure_method = models.CharField(max_length=200, blank=True)
    idcode = models.CharField(max_length=20, blank=True)

    helice = models.ManyToManyField(Helice, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    elTetradoKey = models.CharField(max_length=100)
    base_pair = models.ManyToManyField(BasePair, blank=True)

    r_chie = models.FileField(upload_to="files/results/r_chie/", blank=True)
    r_chie_canonical = models.FileField(
        upload_to="files/results/r_chie-canonical/", blank=True
    )

    varna = models.FileField(upload_to="files/results/varna/", blank=True)
    varna_can = models.FileField(upload_to="files/results/varna-can/", blank=True)
    varna_non_can = models.FileField(
        upload_to="files/results/varna-non-can/", blank=True
    )
    varna_can_non_can = models.FileField(
        upload_to="files/results/varna-can_non-can/", blank=True
    )

    draw_tetrado = models.FileField(upload_to="files/results/layers/", blank=True)

    cached_result = models.TextField(blank=True)

    push_notification = models.ManyToManyField(PushInformation, blank=True)

    error = models.TextField(default="", blank=True)

    def __str__(self):
        return (
            "Request "
            + str(self.id)
            + " ("
            + str(self.source)
            + ") <"
            + str(self.status)
            + "> "
        )


@receiver(pre_delete, sender=TetradoRequest)
def remove_file(**kwargs):
    instance = kwargs.get("instance")
    instance.varna.delete(save=False)
    instance.varna_can.delete(save=False)
    instance.varna_non_can.delete(save=False)
    instance.varna_can_non_can.delete(save=False)
    instance.r_chie.delete(save=False)
    instance.r_chie_canonical.delete(save=False)
    instance.draw_tetrado.delete(save=False)
    for base_pair in instance.base_pair.all():
        base_pair.delete()
    for helice in instance.helice.all():
        helice.delete()


class Log(models.Model):
    type = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    traceback = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Error logs"
        db_table = "webtetrado_logs"
