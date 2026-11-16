import mmcif.io

MODEL_COLUMN = "pdbx_PDB_model_num"
UNKNOWN_VALUES = {".", "?"}


def filter_cif_model(file_absolute_path: str, model_no: int) -> None:
    """Keep only the requested model in an mmCIF file.

    The file is modified in place. Unlike round-tripping through Bio.PDB, this
    only removes ``_atom_site`` rows, so all residue identifiers (label/auth
    chain, component and sequence numbers) are preserved verbatim. This matters
    for modified residues, which Bio.PDB treats as hetero residues and writes
    back as separate chains.
    """
    data = mmcif.io.IoAdapter().readFile(file_absolute_path)
    model = str(model_no)
    filtered = False

    for block in data:
        atom_site = block.getObj("atom_site")
        if atom_site is None:
            continue

        model_index = atom_site.getAttributeIndex(MODEL_COLUMN)
        if model_index == -1:
            if model_no != 1:
                raise ValueError(f"Model {model_no} not found in structure")
            continue

        rows = atom_site.getRowList()
        if not rows:
            continue

        kept = [
            row
            for row in rows
            if str(row[model_index]).strip() == model
            or (model == "1" and str(row[model_index]).strip() in UNKNOWN_VALUES)
        ]
        if not kept:
            raise ValueError(f"Model {model_no} not found in structure")

        if len(kept) != len(rows):
            rows[:] = kept
            filtered = True

    if filtered:
        mmcif.io.IoAdapter().writeFile(file_absolute_path, data)


def filter_pdb_model(file_absolute_path: str, model: int) -> None:
    """Keep only the requested model in a PDB file, in place.

    Header records are retained, and the selected model block is copied without
    being re-serialised, so chain IDs and residue numbers are untouched.
    """
    with open(file_absolute_path, "r") as file:
        lines = file.readlines()

    first_model = next(
        (index for index, line in enumerate(lines) if line.startswith("MODEL")),
        None,
    )
    if first_model is None:
        if model != 1:
            raise ValueError(f"Model {model} not found in structure")
        return

    header = lines[:first_model]
    selected = []
    current_model = None

    for line in lines[first_model:]:
        if line.startswith("MODEL"):
            fields = line.split()
            current_model = int(fields[1]) if len(fields) > 1 else None
            if current_model == model:
                selected.append(line)
        elif line.startswith("ENDMDL"):
            if current_model == model:
                selected.append(line)
            current_model = None
        elif current_model == model:
            selected.append(line)

    if not selected:
        raise ValueError(f"Model {model} not found in structure")

    last_endmdl = max(
        (index for index, line in enumerate(lines) if line.startswith("ENDMDL")),
        default=len(lines) - 1,
    )
    trailer = lines[last_endmdl + 1 :]

    with open(file_absolute_path, "w") as file:
        file.writelines(header + selected + trailer)
