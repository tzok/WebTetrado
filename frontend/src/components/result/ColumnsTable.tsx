import { Table } from "antd";
import { UseAppContext } from "../../AppContextProvider";
import { nucleotide } from "../../types/RestultSet";
import { JsonToCsvButton } from "../services/JsonToCsvButton";

interface ColumnsTableArguments {
  tracts: string[][];
  strandPolarities: (string | null)[][];
  bulges: string[];
  nucleotides: nucleotide[];
  id: boolean;
}

export default function ColumnsTable(props: ColumnsTableArguments) {
  const context = UseAppContext();

  const nucleotideMap = new Map<string, string>();
  props.nucleotides.forEach((nt) => {
    nucleotideMap.set(nt.name, nt.symbol);
  });

  const columnLabels = ["A", "B", "C", "D"];

  const hasAnyBulges = props.bulges && props.bulges.length > 0;

  const dataSource = props.tracts.map((tract, index) => {
    const polarities = props.strandPolarities[index] || [];
    const formattedPolarities = polarities.map((p) => {
      if (p === "plus") return "+";
      if (p === "minus") return "-";
      return "?";
    });

    const tractBulges = tract.filter((nt) => props.bulges.includes(nt));

    const row: Record<string, any> = {
      name: columnLabels[index] || String(index + 1),
      sequence: tract.map((nt) => nucleotideMap.get(nt) || "?").join(""),
      full_sequence: tract.join(", "),
      length: tract.length,
      strand_polarity: formattedPolarities.join(" ") || "?",
    };

    if (hasAnyBulges) {
      row.bulges = tractBulges.join(", ") || "-";
    }

    return row;
  });

  const columns_columns: any[] = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Sequence",
      dataIndex: "sequence",
      key: "sequence",
    },
    {
      title: "Sequence (full names)",
      dataIndex: "full_sequence",
      key: "full_sequence",
    },
    {
      title: "Length",
      dataIndex: "length",
      key: "length",
    },
    {
      title: "Strand polarity",
      dataIndex: "strand_polarity",
      key: "strand_polarity",
      render: (text: string) => (
        <span style={{ fontFamily: "'PT Mono', monospace" }}>{text}</span>
      ),
    },
  ];

  if (hasAnyBulges) {
    columns_columns.push({
      title: "Bulges",
      dataIndex: "bulges",
      key: "bulges",
    });
  }

  const csvFields = ["name", "sequence", "full_sequence", "length", "strand_polarity"];
  const csvHeaders = ["Name", "Sequence", "Sequence (full names)", "Length", "Strand polarity"];

  if (hasAnyBulges) {
    csvFields.push("bulges");
    csvHeaders.push("Bulges");
  }

  return (
    <>
      {dataSource.length > 0 ? (
        <>
          <h2 id={props.id ? "columns" : ""} style={{ marginTop: "40px" }}>
            Columns
          </h2>
          <Table
            style={{ textAlign: "center" }}
            dataSource={dataSource}
            columns={columns_columns}
            scroll={
              !context.viewSettings.isCompressedViewNeeded
                ? { x: "auto" }
                : { x: "100%" }
            }
          />
          <div className="horizontal-center">
            {JsonToCsvButton(
              dataSource,
              csvFields,
              csvHeaders,
              "columns_results"
            )}
          </div>
        </>
      ) : (
        <></>
      )}
    </>
  );
}
