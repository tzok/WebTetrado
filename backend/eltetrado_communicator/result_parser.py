import traceback
import time
import requests
import json
import base64

from backend.models import (
    BasePair,
    Helice,
    Log,
    Loop,
    Metadata,
    Nucleotide,
    Quadruplex,
    Tetrad,
    TetradPair,
    TetradoRequest,
)
from django.core.files.temp import NamedTemporaryFile
from Bio.PDB import PDBParser, MMCIFParser
from backend.file_processor.structure_tetrad_filter import get_cetrain_tetrad_file
from backend.web_push.notification_handler import send_notification_to_subscriber
from WebTetrado.settings import WEBTETRADO_BACKEND_URL
from backend.request_handler.result_composer import compose_json_result
from enum import Enum


class GetterException(Exception):
    """Exception raised for errors caused by insufficient result from webtetrado-backend.

    Attributes:
        operation -- name of processing function
        message -- explanation of the error
    """

    def __init__(self, operation, message="Results are insufficient or improper "):
        self.operation = operation
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.operation} -> {self.message}"


class LwParser(Enum):
    c = "cis"
    t = "trans"
    W = "Watson-Crick-Franklin"
    H = "Hoogsteen"
    S = "Sugar"


def add_base_pairs(base_pairs, tetrado_request):
    base_pair_tetrad = set([])
    for base_pair in base_pairs:
        try:
            if (
                not tuple(sorted((base_pair["nt1"], base_pair["nt2"])))
                in base_pair_tetrad
            ):
                base_pair_tetrad.add(
                    tuple(sorted((base_pair["nt1"], base_pair["nt2"])))
                )
                base_pair_entity = BasePair()
                base_pair_entity.nt1 = Nucleotide.objects.get(
                    query_id=tetrado_request.id, name=base_pair["nt1"]
                )
                base_pair_entity.nt2 = Nucleotide.objects.get(
                    query_id=tetrado_request.id, name=base_pair["nt2"]
                )
                base_pair_entity.edge3 = LwParser[base_pair["lw"][2]].value
                base_pair_entity.edge5 = LwParser[base_pair["lw"][1]].value
                base_pair_entity.stericity = LwParser[base_pair["lw"][0]].value
                base_pair_entity.lw = base_pair["lw"]
                base_pair_entity.canonical = base_pair["canonical"]
                base_pair_entity.inTetrad = base_pair["inTetrad"]
                base_pair_entity.save()
                tetrado_request.base_pair.add(base_pair_entity)
        except Exception:
            tetrado_request.status = 5
            Log.objects.create(
                type="Error [processing_add_base_pairs] ",
                info=str(tetrado_request.id),
                traceback=traceback.format_exc(),
            ).save()
            tetrado_request.error = "Error during adding base pairs."
            tetrado_request.save()
            raise GetterException("Base pair parser", traceback.format_exc())


def add_nucleotides(nucleotides, tetrado_request):
    for nucleotide in nucleotides:
        try:
            nucleotides_entity = Nucleotide()
            nucleotides_entity.query_id = tetrado_request.id
            nucleotides_entity.number = nucleotide["number"]
            nucleotides_entity.symbol = nucleotide["shortName"]
            nucleotides_entity.symbol = nucleotide["shortName"]
            nucleotides_entity.chain = nucleotide["chain"]
            nucleotides_entity.glycosidicBond = nucleotide["glycosidicBond"]
            nucleotides_entity.name = nucleotide["fullName"]
            nucleotides_entity.chi_angle = (
                str(format("%.2f" % nucleotide["chi"])) if "chi" in nucleotide else "-"
            )
            nucleotides_entity.molecule = nucleotide["molecule"]
            nucleotides_entity.save()
        except Exception:
            tetrado_request.status = 5
            Log.objects.create(
                type="Error [processing_add_nucleodities] ",
                info=str(tetrado_request.id),
                traceback=traceback.format_exc(),
            ).save()
            tetrado_request.error = "Error during adding nucleodities."
            tetrado_request.save()
            raise GetterException("Nucleotides parser", traceback.format_exc())


def add_tetrads(quadruplexes, quadruplex_entity, user_request, cif=False):
    for tetrad in quadruplexes:
        try:
            quadruplex_entity_tetrad = Tetrad()
            quadruplex_entity_tetrad_metadata = Metadata()
            quadruplex_entity_tetrad_metadata.tetrad_combination = tetrad[
                "gbaClassification"
            ]
            quadruplex_entity_tetrad_metadata.onz_class = tetrad["onz"]
            quadruplex_entity_tetrad_metadata.save()
            quadruplex_entity_tetrad.metadata = quadruplex_entity_tetrad_metadata
            quadruplex_entity_tetrad.planarity = tetrad["planarityDeviation"]
            quadruplex_entity_tetrad.name = tetrad["id"]
            quadruplex_entity_tetrad.query_id = user_request.id
            quadruplex_entity_tetrad.nt1 = Nucleotide.objects.get(
                query_id=user_request.id, name=tetrad["nt1"]
            )
            quadruplex_entity_tetrad.nt2 = Nucleotide.objects.get(
                query_id=user_request.id, name=tetrad["nt2"]
            )
            quadruplex_entity_tetrad.nt3 = Nucleotide.objects.get(
                query_id=user_request.id, name=tetrad["nt3"]
            )
            quadruplex_entity_tetrad.nt4 = Nucleotide.objects.get(
                query_id=user_request.id, name=tetrad["nt4"]
            )
            quadruplex_entity_tetrad.save()
            if user_request.structure_body is not None:
                get_cetrain_tetrad_file(
                    [
                        quadruplex_entity_tetrad.nt1.name,
                        quadruplex_entity_tetrad.nt2.name,
                        quadruplex_entity_tetrad.nt3.name,
                        quadruplex_entity_tetrad.nt4.name,
                    ],
                    quadruplex_entity_tetrad.tetrad_file,
                    user_request,
                    cif,
                )
            quadruplex_entity_tetrad.save()
            quadruplex_entity.tetrad.add(quadruplex_entity_tetrad)
        except Exception:
            user_request.status = 5
            Log.objects.create(
                type="Error [processing_add_tetrad] ",
                info=str(user_request.id),
                traceback=traceback.format_exc(),
            ).save()
            user_request.error = "Error during adding tetrads."

            user_request.save()
            raise GetterException("Tetrad parser", traceback.format_exc())


def add_loops(loops, quadruplex_entity, user_request):
    for loop in loops:
        try:
            quadruplex_entity_loop = Loop()
            quadruplex_entity_loop.type = loop["type"]
            quadruplex_entity_loop.length = len(loop["nucleotides"])
            quadruplex_entity_loop.save()
            for nucleotide in loop["nucleotides"]:
                quadruplex_entity_loop.nucleotide.add(
                    Nucleotide.objects.get(query_id=user_request.id, name=nucleotide)
                )
            quadruplex_entity_loop.save()
            quadruplex_entity.loop.add(quadruplex_entity_loop)
        except Exception:
            user_request.status = 5
            Log.objects.create(
                type="Error [processing_add_loops] ",
                info=str(user_request.id),
                traceback=traceback.format_exc(),
            ).save()

            user_request.error = "Error during adding loops."
            user_request.save()
            raise GetterException("Loop parser", traceback.format_exc())


def add_tetrad_pairs(tetradPairs, helice_entity, user_request):
    for tetrad_pair in tetradPairs:
        try:
            tetrad_pair_entity = TetradPair()
            tetrad_pair_entity.tetrad1 = Tetrad.objects.get(
                name=tetrad_pair["tetrad1"], query_id=user_request.id
            )
            tetrad_pair_entity.tetrad2 = Tetrad.objects.get(
                name=tetrad_pair["tetrad2"], query_id=user_request.id
            )
            tetrad_pair_entity.rise = tetrad_pair["rise"]
            tetrad_pair_entity.twist = tetrad_pair["twist"]
            tetrad_pair_entity.strand_direction = tetrad_pair["direction"]
            tetrad_pair_entity.save()
            helice_entity.tetrad_pair.add(tetrad_pair_entity)
        except Exception:
            user_request.status = 5
            Log.objects.create(
                type="Error [processing_add_tetrad_pairs] ",
                info=str(user_request.id),
                traceback=traceback.format_exc(),
            ).save()

            user_request.error = "Error during adding tetrad pairs."
            user_request.save()
            break


def add_quadruplexes(quadruplexes, file_data, helice_entity, user_request, cif=False):
    for quadruplex in quadruplexes:
        try:
            quadruplex_entity = Quadruplex()
            quadruplex_entity_metadata = Metadata()
            quadruplex_entity_metadata.tetrad_combination = ", ".join(
                str(x) for x in quadruplex["gbaClassification"]
            )
            quadruplex_entity_metadata.onz_class = (
                quadruplex["onzm"] if "onzm" in quadruplex else "-"
            )
            quadruplex_entity_metadata.save()
            quadruplex_entity.metadata = quadruplex_entity_metadata
            quadruplex_entity.save()

            quadruplex_entity.loop_classification = (
                " ".join(quadruplex["loopClassification"].values())
                if "loopClassification" in quadruplex
                else "-"
            )
            if file_data is not None:
                quadruplex_entity.molecule = file_data.header["head"].upper()
            else:
                quadruplex_entity.molecule = ""
            add_loops(quadruplex["loops"], quadruplex_entity, user_request)
            add_tetrads(
                quadruplex["tetrads"],
                quadruplex_entity,
                user_request,
                cif,
            )
            chains = []
            for tetrad in quadruplex_entity.tetrad.all():
                chains.append(tetrad.nt1.chain)
                chains.append(tetrad.nt2.chain)
                chains.append(tetrad.nt3.chain)
                chains.append(tetrad.nt4.chain)
            tetrads_chains = len(list(set(chains)))
            if tetrads_chains == 1:
                chains_type = "UNI"
            elif tetrads_chains == 2:
                chains_type = "BI"
            elif tetrads_chains == 4:
                chains_type = "TETRA"
            else:
                chains_type = "OTHER"

            quadruplex_entity.type = chains_type
            quadruplex_entity.save()
            helice_entity.quadruplex.add(quadruplex_entity)
        except Exception:
            user_request.status = 5
            Log.objects.create(
                type="Error [processing_add_quadruplexes] ",
                info=str(user_request.id),
                traceback=traceback.format_exc(),
            ).save()

            user_request.error = "Error during adding quadruplexes."
            user_request.save()
            raise GetterException("Quadruplex parser", traceback.format_exc())


def file_downloader(request_key: str, url: str, file_destination):
    while True:
        data_file = NamedTemporaryFile()
        r = requests.get(WEBTETRADO_BACKEND_URL + url)
        data_file.write(r.content)
        file_destination.save(name=request_key + ".svg", content=data_file)
        data_file.close()
        if r.status_code == 200:
            svg_count = str(r.content).count("/>")
            if svg_count < 5:
                file_destination.delete()
            break
        elif r.status_code == 202:
            time.sleep(1)
        else:
            file_destination.delete()
            raise GetterException
            break


def try_download_file(
    request_key: str, url: str, file_destination, user_request, label: str
):
    try:
        file_downloader(request_key, url, file_destination)
        return True
    except Exception:
        Log.objects.create(
            type=f"Warning [download_{label}] ",
            info=str(user_request.id),
            traceback=traceback.format_exc(),
        ).save()
        return False


def parse_result_from_backend(user_request, request_key: str):
    try:
        user_request.elTetradoKey = request_key
        user_request.status = 3

        if user_request.file_extension == "cif":
            parser = MMCIFParser(QUIET=True)
            original_user_structure = parser.get_structure(
                "str", user_request.structure_body_original.path
            )
        elif user_request.file_extension == "pdb":
            parser = PDBParser(PERMISSIVE=True, QUIET=True)
            original_user_structure = parser.get_structure(
                "str", user_request.structure_body_original.path
            )
        elif user_request.file_extension == "test":
            original_user_structure = None
        else:
            raise Exception

        user_request.name = (
            original_user_structure.header["name"].upper()
            if original_user_structure is not None
            and "name" in original_user_structure.header
            else ""
        )
        user_request.structure_method = (
            original_user_structure.header["structure_method"].upper()
            if original_user_structure is not None
            and "structure_method" in original_user_structure.header
            and original_user_structure.header["structure_method"] != "unknown"
            else ""
        )
        user_request.idcode = (
            original_user_structure.header["idcode"].upper()
            if original_user_structure is not None
            and "idcode" in original_user_structure.header
            else ""
        )

        user_request.save()
        while True:
            r = requests.get(WEBTETRADO_BACKEND_URL + "/v1/result/" + request_key)
            if r.status_code == 200:
                result = json.loads(r.content)

                add_nucleotides(result["nucleotides"], user_request)

                for helice in result["helices"]:
                    helice_entity = Helice()
                    helice_entity.save()
                    add_quadruplexes(
                        helice["quadruplexes"],
                        original_user_structure,
                        helice_entity,
                        user_request,
                        user_request.file_extension == "cif",
                    )
                    add_tetrad_pairs(helice["tetradPairs"], helice_entity, user_request)
                    user_request.helice.add(helice_entity)
                add_base_pairs(result["basePairs"], user_request)
                user_request.dot_bracket_line1 = result["dotBracket"]["line1"]
                user_request.dot_bracket_line2 = result["dotBracket"]["line2"]
                user_request.dot_bracket_sequence = result["dotBracket"]["sequence"]
                canonical = False
                non_canonical = False

                for base_pair in user_request.base_pair.all():
                    if not base_pair.inTetrad and base_pair.canonical:
                        canonical = True
                    if not base_pair.inTetrad and not base_pair.canonical:
                        non_canonical = True
                    if canonical and non_canonical:
                        break

                try_download_file(
                    request_key,
                    "/v1/varna/" + request_key + "?canonical=false&non-canonical=false",
                    user_request.varna,
                    user_request,
                    "varna",
                )
                if canonical:
                    try_download_file(
                        request_key,
                        "/v1/varna/"
                        + request_key
                        + "?canonical=true&non-canonical=false",
                        user_request.varna_can,
                        user_request,
                        "varna_can",
                    )
                if non_canonical:
                    try_download_file(
                        request_key,
                        "/v1/varna/"
                        + request_key
                        + "?canonical=false&non-canonical=true",
                        user_request.varna_non_can,
                        user_request,
                        "varna_non_can",
                    )
                if canonical and non_canonical:
                    try_download_file(
                        request_key,
                        "/v1/varna/"
                        + request_key
                        + "?canonical=true&non-canonical=true",
                        user_request.varna_can_non_can,
                        user_request,
                        "varna_can_non_can",
                    )

                try_download_file(
                    request_key,
                    "/v1/r-chie/" + request_key + "?canonical=false",
                    user_request.r_chie,
                    user_request,
                    "r_chie",
                )
                if canonical:
                    try_download_file(
                        request_key,
                        "/v1/r-chie/" + request_key + "?canonical=true",
                        user_request.r_chie_canonical,
                        user_request,
                        "r_chie_canonical",
                    )
                try_download_file(
                    request_key,
                    "/v1/draw-tetrado/" + request_key,
                    user_request.draw_tetrado,
                    user_request,
                    "draw_tetrado",
                )

                user_request.status = 4
                user_request.save()

                user_request.cached_result = compose_json_result(user_request.id)
                user_request.save()
                payload = {
                    "image": "https://webtetrado.cs.put.poznan.pl/static/logo.svg",
                    "tag": "Complete",
                    "url": "https://webtetrado.cs.put.poznan.pl/result/"
                    + str(user_request.hash_id),
                    "title": "WebTetrado notification",
                    "text": "Processing of "
                    + str(user_request.hash_id)
                    + " has been completed",
                }
                for subscriber in TetradoRequest.objects.get(
                    id=user_request.id
                ).push_notification.all():
                    send_notification_to_subscriber(
                        subscriber, json.dumps(payload), ttl=3600
                    )
                break
            if r.status_code == 500:
                user_request.status = 5
                user_request.error = "ElTetrado processor error."
                user_request.save()
                break
            time.sleep(1)
    except Exception:
        user_request.status = 5
        user_request.error = "ElTetrado processor error."
        user_request.save()
        Log.objects.create(
            type="Error [parsing] ",
            info=str(user_request.id),
            traceback=traceback.format_exc(),
        ).save()
        return False
    return True


def add_task_to_queue(user_request):
    try:
        with open(user_request.structure_body.path, "rb") as structure_file:
            base64file = base64.b64encode(structure_file.read())

        r = requests.post(
            WEBTETRADO_BACKEND_URL + "/v1/structure",
            data=json.dumps(
                {
                    "pdb_mmcif_b64": str(base64file.decode("utf-8")),
                    "noReorder": user_request.no_reorder,
                    "analyzer": user_request.analyzer,
                    "model": user_request.model,
                }
            ),
            headers={"Content-Type": "application/json"},
            timeout=60,
        )

        begin = time.time()

        while r.status_code != 200:
            if time.time() - begin > 60:
                user_request.status = 5
                user_request.error = (
                    "Timed out waiting for WebTetrado backend task creation."
                )
                user_request.save()
                return False
            if r.status_code >= 400:
                user_request.status = 5
                try:
                    error_payload = r.json()
                    user_request.error = error_payload.get(
                        "errorMessage", "Failed to create WebTetrado backend task."
                    )
                except Exception:
                    user_request.error = f"Failed to create WebTetrado backend task: HTTP {r.status_code}"
                user_request.save()
                return False
            time.sleep(2)

        if r.status_code == 200:
            payload = json.loads(r.content)
            request_key = payload.get("structureId") or payload.get("structure_id")
            if not request_key:
                user_request.status = 5
                user_request.error = f"Failed to read WebTetrado backend task id: {json.dumps(payload)[:900]}"
                user_request.save()
                return False
            return parse_result_from_backend(user_request, request_key)
        else:
            user_request.status = 5
            user_request.error = "Failed to create WebTetrado backend task."
            user_request.save()
            return False
    except Exception:
        user_request.status = 5
        user_request.error = traceback.format_exc().splitlines()[-1][:1000]

        Log.objects.create(
            type="Error [processing] ",
            info=str(user_request.id),
            traceback=traceback.format_exc(),
        ).save()
        user_request.save()
