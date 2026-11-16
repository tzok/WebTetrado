from types import SimpleNamespace

from django.core.files.temp import NamedTemporaryFile
from django.test import TestCase
import mmcif.io
import requests

from WebTetrado.settings import BASE_DIR
from backend.file_processor.structure_model_filter import (
    filter_cif_model,
    filter_pdb_model,
)
from backend.file_processor.structure_tetrad_filter import get_cetrain_tetrad_file

CIF_RESIDUE_COLUMNS = (
    "auth_asym_id",
    "label_asym_id",
    "auth_comp_id",
    "label_comp_id",
    "auth_seq_id",
    "label_seq_id",
    "pdbx_PDB_ins_code",
    "pdbx_PDB_model_num",
)


def cif_residues(path):
    data = mmcif.io.IoAdapter().readFile(path)
    atom_site = data[0].getObj("atom_site")
    indexes = {name: atom_site.getAttributeIndex(name) for name in CIF_RESIDUE_COLUMNS}
    residues = set()
    models = set()
    for row in atom_site.getRowList():
        if indexes["pdbx_PDB_model_num"] != -1:
            models.add(str(row[indexes["pdbx_PDB_model_num"]]).strip())
        residue = []
        for name in CIF_RESIDUE_COLUMNS[:-1]:
            value = str(row[indexes[name]]).strip()
            if name == "pdbx_PDB_ins_code" and value in {".", "?"}:
                value = ""
            residue.append(value)
        residues.add(tuple(residue))
    return models, residues


def auth_residues(residues):
    return {
        (auth_chain, auth_comp, auth_number, icode)
        for auth_chain, label_chain, auth_comp, label_comp, auth_number, label_number, icode in residues
    }


def pdb_residues(path):
    residues = set()
    with open(path) as file:
        for line in file:
            if line.startswith(("ATOM", "HETATM")):
                residues.add(
                    (
                        line[21],
                        line[17:20].strip(),
                        line[22:26].strip(),
                        line[26].strip(),
                    )
                )
    return residues


class FakeSavedFile:
    def save(self, name, file):
        self.name = name
        self.content = file.read()


class StructureParserTest(TestCase):
    def download(self, pdb_id, extension):
        response = requests.get(
            f"http://files.rcsb.org/download/{pdb_id}.{extension}",
            allow_redirects=True,
        )
        self.assertTrue(response.status_code == 200, msg="RCSB server not responds")
        structure_file = NamedTemporaryFile()
        structure_file.write(response.content)
        structure_file.flush()
        return structure_file

    def fixture(self, name):
        return str(BASE_DIR) + "/backend/tests/test_files/" + name

    def assert_cif_model(self, pdb_id, fixture_name):
        structure_file = self.download(pdb_id, "cif")
        filter_cif_model(structure_file.name, 1)

        models, residues = cif_residues(structure_file.name)
        fixture_models, fixture_residues_set = cif_residues(self.fixture(fixture_name))

        self.assertEqual(models, {"1"})
        self.assertEqual(fixture_models, {"1"})
        self.assertEqual(auth_residues(residues), auth_residues(fixture_residues_set))

    def assert_pdb_model(self, pdb_id, fixture_name):
        structure_file = self.download(pdb_id, "pdb")
        filter_pdb_model(structure_file.name, 1)

        self.assertEqual(
            pdb_residues(structure_file.name),
            pdb_residues(self.fixture(fixture_name)),
        )

    def test_give6rs3Cif_doFilterModel_getFilteredFirstModel(self):
        self.assert_cif_model("6rs3", "6rs3_1.cif")

    def test_give6rs3Pdb_doFilterModel_getFilteredFirstModel(self):
        self.assert_pdb_model("6rs3", "6rs3_1.pdb")

    def test_give2hy9Cif_doFilterModel_getFilteredFirstModel(self):
        self.assert_cif_model("2hy9", "2hy9_1.cif")

    def test_give2hy9Pdb_doFilterModel_getFilteredFirstModel(self):
        self.assert_pdb_model("2hy9", "2hy9_1.pdb")

    def test_give6r9kCif_doFilterModel_modifiedResiduesKeepNumbering(self):
        structure_file = self.download("6r9k", "cif")
        filter_cif_model(structure_file.name, 1)

        models, residues = cif_residues(structure_file.name)

        self.assertEqual(models, {"1"})
        self.assertIn(
            ("A", "A", "DG", "DG", "5", "5", ""),
            residues,
        )
        self.assertIn(
            ("A", "A", "BGM", "BGM", "6", "6", ""),
            residues,
        )
        self.assertIn(
            ("A", "A", "BGM", "BGM", "7", "7", ""),
            residues,
        )
        self.assertEqual(len(residues), 25)

        # Modified residues must not be split into separate label chains, as
        # that makes MAXIT treat them as ligands and renumber them.
        label_chains = {residue[1] for residue in residues}
        self.assertEqual(label_chains, {"A"})

    def test_give6r9kCif_tetradExtraction_keepsNumbering(self):
        structure_file = self.download("6r9k", "cif")
        filter_cif_model(structure_file.name, 1)

        saved = FakeSavedFile()
        request = SimpleNamespace(
            structure_body=SimpleNamespace(path=structure_file.name)
        )
        get_cetrain_tetrad_file(
            ["A.DG5", "A.BGM6", "A.BGM7", "A.DT8"],
            saved,
            request,
            cif=True,
        )

        with NamedTemporaryFile() as filtered:
            filtered.write(saved.content)
            filtered.flush()
            _, residues = cif_residues(filtered.name)

        self.assertEqual({residue[4] for residue in residues}, {"5", "6", "7", "8"})
        self.assertEqual({residue[1] for residue in residues}, {"A"})
