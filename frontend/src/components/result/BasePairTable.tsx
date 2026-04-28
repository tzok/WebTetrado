import { Table } from "antd";
import { UseAppContext } from "../../AppContextProvider";
import { base_pair } from "../../types/RestultSet";
import { JsonToCsvButton } from "../services/JsonToCsvButton";

interface BasePairTableArguents {
    value: base_pair[];
    id: boolean;
}
export default function BasePairTable(props: BasePairTableArguents) {
    const context = UseAppContext();
    const columns_base_pairs = [
        {
            title: "Number",
            dataIndex: "number",
            key: "number",
            sorter: (a: any, b: any) => {
                return a.number - b.number;
            },
        },
        {
            title: "Nucleotide 1",
            dataIndex: "nt1",
            key: "nt1",
        },
        {
            title: "Nucleotide 2",
            dataIndex: "nt2",
            key: "nt2",
        },
        {
            title: "Leontis-Westhof notation",
            dataIndex: "lw",
            key: "lw",
        },
        {
            title: "In tetrad",
            dataIndex: "in_tetrad",
            key: "in_tetrad",
            sorter: (a: any, b: any) => {
                if (a.in_tetrad == b.in_tetrad) return 0;
                if (a.in_tetrad) return 1;
                else return -1;
            },
            render: (be: boolean) => <>{be ? <>✅</>: ""}</>,
        },
    ];
    return (
        <>
            <h2 id={props.id ? "base-pairs" : ""} style={{ marginTop: "40px" }}>
                Base pairs
            </h2>

            <Table
                style={{ textAlign: "center" }}
                dataSource={props.value}
                columns={columns_base_pairs}
                scroll={
                    !context.viewSettings.isCompressedViewNeeded
                        ? { x: "auto" }
                        : { x: "100%" }
                }
            />
            <div className="horizontal-center">
                {JsonToCsvButton(props.value, ['number', 'nt1', 'nt2', 'lw', 'in_tetrad'], ['Number', 'Nucleotide 1', 'Nucleotide 2', 'Leontis-Westhof notation', 'In tetrad'], 'base_pair_results')}
            </div>
        </>
    );
}
