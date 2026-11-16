import re
from tempfile import NamedTemporaryFile
from typing import List, Optional, Tuple

import mmcif.io

ResidueId = Tuple[Optional[str], str, str, Optional[str]]

UNKNOWN_VALUES = {".", "?", ""}


def _parse_residue_id(identifier: str) -> Optional[ResidueId]:
    """Parse a residue identifier used by ElTetrado, e.g. ``A.DG/5`` or ``DG5``."""
    chain = None
    rest = identifier.strip()

    if "." in rest:
        chain, rest = rest.split(".", 1)

    icode = None
    if "^" in rest:
        rest, icode = rest.split("^", 1)

    if "/" in rest:
        comp, number = rest.rsplit("/", 1)
    else:
        match = re.match(r"^(.*?)(-?\d+)$", rest)
        if match is None:
            return None
        comp, number = match.group(1), match.group(2)

    if not comp or not number:
        return None

    return (chain or None), comp, number, (icode or None)


def _parse_residue_ids(identifiers: List[str]) -> List[ResidueId]:
    parsed = [_parse_residue_id(identifier) for identifier in identifiers]
    return [residue_id for residue_id in parsed if residue_id is not None]


def _cif_row_matches(row: list, indexes: dict, residue_ids: List[ResidueId]) -> bool:
    icode = (
        str(row[indexes["pdbx_PDB_ins_code"]]).strip()
        if indexes["pdbx_PDB_ins_code"] != -1
        else ""
    )
    if icode in UNKNOWN_VALUES:
        icode = ""

    candidates = []
    for chain_column, comp_column, number_column in (
        ("auth_asym_id", "auth_comp_id", "auth_seq_id"),
        ("label_asym_id", "label_comp_id", "label_seq_id"),
    ):
        if any(
            indexes[name] == -1 for name in (chain_column, comp_column, number_column)
        ):
            continue
        candidates.append(
            (
                str(row[indexes[chain_column]]).strip(),
                str(row[indexes[comp_column]]).strip(),
                str(row[indexes[number_column]]).strip(),
                icode,
            )
        )

    for wanted_chain, wanted_comp, wanted_number, wanted_icode in residue_ids:
        for chain, comp, number, row_icode in candidates:
            if wanted_chain is not None and wanted_chain != chain:
                continue
            if comp != wanted_comp or number != wanted_number:
                continue
            if wanted_icode is not None and wanted_icode != row_icode:
                continue
            return True

    return False


def _filter_cif_residues(
    source_path: str, output_path: str, residue_ids: List[ResidueId]
) -> None:
    data = mmcif.io.IoAdapter().readFile(source_path)
    columns = (
        "auth_asym_id",
        "label_asym_id",
        "auth_comp_id",
        "label_comp_id",
        "auth_seq_id",
        "label_seq_id",
        "pdbx_PDB_ins_code",
    )

    for block in data:
        atom_site = block.getObj("atom_site")
        if atom_site is None:
            continue

        indexes = {name: atom_site.getAttributeIndex(name) for name in columns}
        rows = atom_site.getRowList()
        rows[:] = [row for row in rows if _cif_row_matches(row, indexes, residue_ids)]

    mmcif.io.IoAdapter().writeFile(output_path, data)


def _pdb_line_matches(line: str, residue_ids: List[ResidueId]) -> bool:
    chain = line[21].strip() or None
    comp = line[17:20].strip()
    number = line[22:26].strip()
    icode = line[26].strip() or None

    for wanted_chain, wanted_comp, wanted_number, wanted_icode in residue_ids:
        if wanted_chain is not None and wanted_chain != chain:
            continue
        if comp != wanted_comp or number != wanted_number:
            continue
        if wanted_icode is not None and wanted_icode != icode:
            continue
        return True

    return False


def _filter_pdb_residues(
    source_path: str, output_path: str, residue_ids: List[ResidueId]
) -> None:
    with open(source_path, "r") as source:
        lines = [
            line
            for line in source
            if line.startswith(("ATOM", "HETATM"))
            and _pdb_line_matches(line, residue_ids)
        ]

    with open(output_path, "w") as output:
        output.writelines(lines)
        output.write("END\n")


def get_cetrain_tetrad_file(
    tetrad_residue: List[str], tetrad_result_file, user_request, cif=True
):
    if not user_request.structure_body:
        return

    residue_ids = _parse_residue_ids(tetrad_residue)
    if not residue_ids:
        return

    suffix = ".cif" if cif else ".pdb"
    tetrad_file = NamedTemporaryFile(suffix=suffix)

    if cif:
        _filter_cif_residues(
            user_request.structure_body.path, tetrad_file.name, residue_ids
        )
    else:
        _filter_pdb_residues(
            user_request.structure_body.path, tetrad_file.name, residue_ids
        )

    tetrad_file.seek(0)
    tetrad_result_file.save(
        "-".join(tetrad_residue).replace(".", "_").replace("/", "-") + suffix,
        tetrad_file,
    )
    tetrad_file.close()
