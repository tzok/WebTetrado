import filecmp
from backend.tests.compare_json_files import compare
from django.core.files.temp import NamedTemporaryFile
from django.test import TestCase
from backend.eltetrado_communicator.result_parser import parse_result_from_backend
from backend.models import TetradoRequest
from backend.request_handler.result_composer import compose_json_result
import httpretty
from WebTetrado.settings import WEBTETRADO_BACKEND_URL
from WebTetrado.settings import BASE_DIR


class ResultComposerTest(TestCase):
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

    @httpretty.activate
    def test_get1JJP1_doComposeJSONResult_resultProperResult(self):
        self.setUpTest("code_1jjp")
        httpretty.register_uri(
            httpretty.GET,
            str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_1jjp",
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
        entity.complete_2d = False
        entity.no_reorder = False
        entity.g4_limited = False
        entity.model = 1
        entity.status = 1
        entity.source = 1
        entity.file_extension = "test"
        entity.save()
        parse_result_from_backend(entity, "code_1jjp")
        data_file = NamedTemporaryFile()
        data_file.write(bytes(compose_json_result(entity.id), "UTF-8"))
        self.assertTrue(
            compare(
                data_file.name,
                str(BASE_DIR) + "/backend/tests/test_files/1jjp_1_cache.json",
                ["remove_date"],
            )
        )
        data_file.close()
        entity.delete()

    @httpretty.activate
    def test_get2HY91_doComposeJSONResult_resultProperResult(self):
        self.setUpTest("code_2hy9")
        httpretty.register_uri(
            httpretty.GET,
            str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_2hy9",
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
        entity.file_extension = "test"
        entity.save()
        parse_result_from_backend(entity, "code_2hy9")
        data_file = NamedTemporaryFile()
        data_file.write(bytes(compose_json_result(entity.id), "UTF-8"))
        self.assertTrue(
            compare(
                data_file.name,
                str(BASE_DIR) + "/backend/tests/test_files/2hy9_1_cache.json",
                ["remove_date"],
            )
        )
        data_file.close()
        entity.delete()

    @httpretty.activate
    def test_get6RS31_doComposeJSONResult_resultProperResult(self):
        self.setUpTest("code_6rs3")
        httpretty.register_uri(
            httpretty.GET,
            str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_6rs3",
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
        entity.file_extension = "test"
        entity.save()
        parse_result_from_backend(entity, "code_6rs3")
        data_file = NamedTemporaryFile()
        data_file.write(bytes(compose_json_result(entity.id), "UTF-8"))
        self.assertTrue(
            compare(
                data_file.name,
                str(BASE_DIR) + "/backend/tests/test_files/6rs3_1_cache.json",
                ["remove_date"],
            )
        )
        data_file.close()
        entity.delete()

    @httpretty.activate
    def test_get6FC91_doComposeJSONResult_resultProperResult(self):
        self.setUpTest("code_6fc9")
        httpretty.register_uri(
            httpretty.GET,
            str(WEBTETRADO_BACKEND_URL) + "/v1/result/" + "code_6fc9",
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
        entity.file_extension = "test"
        entity.save()
        parse_result_from_backend(entity, "code_6fc9")
        data_file = NamedTemporaryFile()
        data_file.write(bytes(compose_json_result(entity.id), "UTF-8"))
        self.assertTrue(
            compare(
                data_file.name,
                str(BASE_DIR) + "/backend/tests/test_files/6fc9_1_cache.json",
                ["remove_date"],
            )
        )
        data_file.close()
        entity.delete()
