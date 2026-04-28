import json
from django.contrib import admin
from backend.web_push.notification_handler import send_notification_to_subscriber
from backend.models import (
    Helice,
    Loop,
    Metadata,
    Nucleotide,
    PushInformation,
    Quadruplex,
    TemporaryFile,
    Tetrad,
    TetradPair,
    TetradoRequest,
    BasePair,
    Log,
)


@admin.register(TemporaryFile)
class TemporaryFiles(admin.ModelAdmin):
    list_display = ("id", "file", "file_extension", "timestamp")


@admin.register(TetradoRequest)
class TetradoRequest(admin.ModelAdmin):
    list_display = (
        "id",
        "source",
        "status",
        "timestamp",
        "structure_body",
        "structure_body",
        "hash_id",
        "draw_tetrado",
        "no_reorder",
        "model",
        "elTetradoKey",
    )


@admin.register(Quadruplex)
class Quadruplex(admin.ModelAdmin):
    list_display = ("id", "molecule", "type", "loop_classification", "metadata")


@admin.register(Helice)
class Helice(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(BasePair)
class Base_Pair(admin.ModelAdmin):
    list_display = ("id", "nt1", "nt2", "edge3", "edge5", "stericity")


@admin.register(Loop)
class Loop(admin.ModelAdmin):
    list_display = ("id", "type", "length")


@admin.register(TetradPair)
class Tetrad_Pair(admin.ModelAdmin):
    list_display = ("id", "tetrad1", "tetrad2", "rise", "twist", "strand_direction")


@admin.register(Tetrad)
class Tetrad(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "query_id",
        "planarity",
        "metadata",
        "nt1",
        "nt2",
        "nt3",
        "nt4",
        "tetrad_file",
    )


@admin.register(Nucleotide)
class Nucleotide(admin.ModelAdmin):
    list_display = ("id", "number", "symbol", "chain", "name", "chi_angle", "molecule")


@admin.register(Metadata)
class Metadata(admin.ModelAdmin):
    list_display = (
        "id",
        "onz_class",
        "tetrad_combination",
    )


@admin.register(PushInformation)
class PushInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "hash_id", "browser", "user_agent")
    actions = ("send_test_message",)

    def send_test_message(self, request, queryset):
        payload = {"head": "Hey", "body": "Hello World"}
        for device in queryset:
            notification = send_notification_to_subscriber(
                device, json.dumps(payload), 0
            )
            if notification:
                self.message_user(request, "Test sent successfully")
            else:
                self.message_user(request, "Deprecated subscription deleted")


@admin.register(Log)
class Log(admin.ModelAdmin):
    list_display = ("type", "info", "timestamp")
