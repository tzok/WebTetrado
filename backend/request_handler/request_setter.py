import django_rq
import requests
import os
from typing import Dict
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse
from rq import Retry
from backend.models import TemporaryFile, TetradoRequest
from WebTetrado import settings
from backend.eltetrado_communicator.result_parser import add_task_to_queue
from backend.file_processor.structure_model_filter import (
    filter_cif_model,
    filter_pdb_model,
)


def set_user_request_action(body: Dict):
    entity = TetradoRequest()
    entity.no_reorder = not body["settings"]["reorder"]
    entity.g4_limited = body["settings"]["g4Limited"]
    entity.model = body["settings"]["model"]
    entity.status = 1

    if "fileId" in body and len(body["fileId"]) > 0:
        entity.source = 2
        if body["fileId"].split("_")[0] == "rdy":
            file_name = body["fileId"].split("_")
            try:
                temp_file = open(
                    os.path.join(
                        settings.BASE_DIR,
                        "example_structure_files/"
                        + file_name[1].split("/")[-1]
                        + "."
                        + file_name[2],
                    ),
                    "rb",
                )
                entity.structure_body.save(
                    name=temp_file.name.split("/")[-1], content=temp_file
                )
                entity.structure_body_original.save(
                    name=temp_file.name.split("/")[-1], content=temp_file
                )
                entity.file_extension = file_name[2]
            except FileNotFoundError:
                return HttpResponse(status=400)
        else:
            temp_file = TemporaryFile.objects.get(id=body["fileId"])
            entity.structure_body.save(
                name=temp_file.file.name.split("/")[-1],
                content=temp_file.file.open("rb"),
            )
            entity.structure_body_original.save(
                name=temp_file.file.name.split("/")[-1],
                content=temp_file.file.open("rb"),
            )
            entity.file_extension = temp_file.file_extension
            TemporaryFile.objects.get(id=body["fileId"]).delete()
    elif "rcsbPdbId" in body and len(body["rcsbPdbId"]) > 0:
        url = "http://files.rcsb.org/download/" + body["rcsbPdbId"] + ".cif"
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            data_file = NamedTemporaryFile()
            data_file.write(r.content)
            entity.source = 1
            entity.file_extension = "cif"
            entity.structure_body.save(
                name=body["rcsbPdbId"] + ".cif", content=data_file
            )
            entity.structure_body_original.save(
                name=body["rcsbPdbId"] + ".cif", content=data_file
            )
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=500)

    entity.save()

    try:
        if entity.file_extension == "cif":
            filter_cif_model(entity.structure_body.path, entity.model)
        elif entity.file_extension == "pdb":
            filter_pdb_model(entity.structure_body.path, entity.model)
    except Exception:
        entity.status = 5
        entity.error = "Model does not exist"
        entity.save()
        return HttpResponse(status=500)

    entity.status = 2
    entity.save()

    queue = django_rq.get_queue("default", is_async=True)
    queue.enqueue(add_task_to_queue, entity, retry=Retry(max=3))
    return HttpResponse(
        content=b'{"orderId":"' + bytes(str(entity.hash_id), "UTF-8") + b'"}',
        content_type="application/json",
    )
