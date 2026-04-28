from Bio.PDB import MMCIFIO
from Bio.PDB.MMCIFParser import MMCIFParser
from django.test import TestCase
from backend.eltetrado_communicator.result_parser import parse_result_from_backend
from backend.models import TetradoRequest
import httpretty
from WebTetrado.settings import WEBTETRADO_BACKEND_URL
from WebTetrado.settings import BASE_DIR


class ResultParserTest(TestCase):
    def tearDown(self) -> None:
        httpretty.reset()
        return super().tearDown()

    def setUpTest(self, name: str):
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL) + "/v1/draw-tetrado/" + name,
            status=200,
            body="",
        )
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL) + "/v1/r-chie/" + name + "?canonical=false",
            status=200,
            body="",
        )
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL) + "/v1/r-chie/" + name + "?canonical=true",
            status=200,
            body="",
        )
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL)
            + "/v1/varna/"
            + name
            + "?canonical=false&non-canonical=false",
            status=200,
            body="",
        )
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL)
            + "/v1/varna/"
            + name
            + "?canonical=false&non-canonical=true",
            status=200,
            body="",
        )
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL)
            + "/v1/varna/"
            + name
            + "?canonical=true&non-canonical=false",
            status=200,
            body="",
        )
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL)
            + "/v1/varna/"
            + name
            + "?canonical=true&non-canonical=true",
            status=200,
            body="",
        )

    def tetrad_file_residue_check(self, entity):
        io = MMCIFIO()
        for i in entity.helice.all():
            for j in i.quadruplex.all():
                for k in j.tetrad.all():
                    io.set_structure(
                        MMCIFParser(QUIET=True).get_structure("str", k.tetrad_file.path)
                    )
                    self.assertEqual(
                        len(list(set([i.id[1] for i in io.structure.get_residues()]))),
                        4,
                        " ".join([str(i) for i in io.structure.get_residues()]),
                    )

    @httpretty.activate
    def test_get1JJP1_doParseToDatabase_resultSuccess(self):
        self.setUpTest("code_1jjp")
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_1jjp",
            status=200,
            body="".join(
                [
                    i
                    for i in open(
                        str(BASE_DIR) + "/backend/tests/test_files/1jjp_1.json", "r"
                    )
                ]
            ),
        )
        entity = TetradoRequest()
        entity.no_reorder = False
        entity.g4_limited = False
        entity.model = 1
        entity.status = 1
        entity.source = 1
        entity.file_extension = "cif"
        entity.complete_2d = False
        entity.structure_body.save(
            name="code_1jjp",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/1jjp_1.cif", "rb"),
        )
        entity.structure_body_original.save(
            name="code_1jjp",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/1jjp.cif", "rb"),
        )
        entity.save()
        self.assertTrue(parse_result_from_backend(entity, "code_1jjp"))
        self.tetrad_file_residue_check(entity)
        entity.delete()

    @httpretty.activate
    def test_get2HY91_doParseToDatabase_resultSuccess(self):
        self.setUpTest("code_2hy9")
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_2hy9",
            status=200,
            body="".join(
                [
                    i
                    for i in open(
                        str(BASE_DIR) + "/backend/tests/test_files/2hy9_1.json", "r"
                    )
                ]
            ),
        )
        entity = TetradoRequest()
        entity.complete_2d = False
        entity.no_reorder = False
        entity.g4_limited = False
        entity.model = 1
        entity.status = 1
        entity.source = 1
        entity.file_extension = "cif"
        entity.save()
        entity.structure_body.save(
            name="code_2hy9",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/2hy9_1.cif", "rb"),
        )
        entity.structure_body_original.save(
            name="code_2hy9",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/2hy9.cif", "rb"),
        )
        self.assertTrue(parse_result_from_backend(entity, "code_2hy9"))
        self.tetrad_file_residue_check(entity)
        entity.delete()

    @httpretty.activate
    def test_get6RS31_doParseToDatabase_resultSuccess(self):
        self.setUpTest("code_6rs3")
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_6rs3",
            status=200,
            body="".join(
                [
                    i
                    for i in open(
                        str(BASE_DIR) + "/backend/tests/test_files/6rs3_1.json", "r"
                    )
                ]
            ),
        )
        entity = TetradoRequest()
        entity.complete_2d = False
        entity.no_reorder = False
        entity.g4_limited = False
        entity.model = 1
        entity.status = 1
        entity.source = 1
        entity.file_extension = "cif"
        entity.structure_body.save(
            name="code_6rs3",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/6rs3_1.cif", "rb"),
        )
        entity.structure_body_original.save(
            name="code_6rs3",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/6rs3.cif", "rb"),
        )
        entity.save()
        self.assertTrue(parse_result_from_backend(entity, "code_6rs3"))
        self.tetrad_file_residue_check(entity)
        entity.delete()

    @httpretty.activate
    def test_get6FC91_doParseToDatabase_resultSuccess(self):
        self.setUpTest("code_6fc9")
        httpretty.register_uri(
            method=httpretty.GET,
            uri=str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_6fc9",
            status=200,
            body="".join(
                [
                    i
                    for i in open(
                        str(BASE_DIR) + "/backend/tests/test_files/6fc9_1.json", "r"
                    )
                ]
            ),
        )
        entity = TetradoRequest()
        entity.complete_2d = False
        entity.no_reorder = False
        entity.g4_limited = False
        entity.model = 1
        entity.status = 1
        entity.source = 1
        entity.file_extension = "cif"
        entity.structure_body.save(
            name="code_6fc9",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/6fc9_1.cif", "rb"),
        )
        entity.structure_body_original.save(
            name="code_6fc9",
            content=open(str(BASE_DIR) + "/backend/tests/test_files/6fc9.cif", "rb"),
        )
        entity.save()
        self.assertTrue(parse_result_from_backend(entity, "code_6fc9"))
        self.tetrad_file_residue_check(entity)
        entity.delete()
