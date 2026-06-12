import { Table } from "antd";
import { UseAppContext } from "../../AppContextProvider";
import { nucleotide } from "../../types/RestultSet";
import { JsonToCsvButton } from "../services/JsonToCsvButton";

interface NucleotideTableArguemnts {
    value: nucleotide[];
    id: boolean;
}
export default function NucleotideTable(props: NucleotideTableArguemnts) {
    const context = UseAppContext();
    const columns_nucleotides = [
        {
            title: "Number",
            dataIndex: "number",
            key: "number",
        },
        {
            title: "Symbol",
            dataIndex: "symbol",
            key: "symbol",
        },
        {
            title: "Full name",
            dataIndex: "name",
            key: "name",
        },
        {
            title: "Chi angle (value) [°]",
            dataIndex: "chi_angle",
            key: "chi_angle",
        },
        {
            title: "Chi angle (type)",
            dataIndex: "glycosidicBond",
            key: "glycosidicBond",
        },
        {
            title: "Sugar pucker",
            dataIndex: "sugar_pucker",
            key: "sugar_pucker",
        },
    ];
    return (
        <>
            <h2 id={props.id ? "nucleotides" : ""} style={{ marginTop: "40px" }}>
                Nucleotides
            </h2>
            <Table
                style={{ textAlign: "center" }}
                dataSource={props.value}
                scroll={
                    !context.viewSettings.isCompressedViewNeeded
                        ? { x: "auto" }
                        : { x: "100%" }
                }
                columns={columns_nucleotides}
            />
            <div className="horizontal-center">
                {JsonToCsvButton(props.value, ['number', 'symbol', 'name', 'chi_angle', 'glycosidicBond', 'sugar_pucker'], ['Number', 'Symbol', 'Full name', 'Chi angle (value) [°]', 'Chi angle (type)', 'Sugar pucker'], 'nucleotide_results')}
            </div>
        </>
    );
}
