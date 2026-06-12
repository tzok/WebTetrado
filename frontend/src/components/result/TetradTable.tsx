import { Button, Table, Tooltip, Image } from "antd";
import { tetrad } from "../../types/RestultSet";
import { DownloadOutlined } from "@ant-design/icons";
import { UseAppContext } from "../../AppContextProvider";
import { JsonToCsvButton } from "../services/JsonToCsvButton";
import { InfoCircleOutlined } from "@ant-design/icons";
interface TetradTableArguments {
  value: tetrad[];
  g4Limited: boolean;
  id: boolean;
  tetradPolarities?: (string | null)[];
}
export default function TetradTable(props: TetradTableArguments) {
  const context = UseAppContext();
  const columns_tetrad = [
    {
      title: "Number",
      dataIndex: "number",
      key: "number",
    },
    {
      title: "Sequence",
      dataIndex: "sequence",
      key: "sequence",
    },
    {
      title: "Sequence (full names)",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "ONZ class",
      dataIndex: "onz_class",
      key: "onz_class",
    },
    {
      title: "Tetrad combination",
      dataIndex: "gbaClassification",
      key: "gbaClassification",
      render: (text: string) => (
        <>
          <Tooltip
            title={
              <Image
                alt={"da-silva" + text}
                src={require("../../assets/da-silva/" + text + ".svg")}
              />
            }
            color={"white"}
          >
            <u>{text}</u>
            <sup><InfoCircleOutlined rev={undefined} style={{ color: '#0272b4' }} /></sup>
          </Tooltip>
        </>
      ),
    },
    {
      title: "Planarity [Å]",
      dataIndex: "planarity",
      key: "planarity",
    },
    {
      title: "Tetrad polarity",
      dataIndex: "tetrad_polarity",
      key: "tetrad_polarity",
    },
    {
      title: "Download",
      dataIndex: "file",
      key: "file",
      render: (text: string) => (
        <>
          {text.length > 0 ? (
            <a href={text}>
              <Button type="primary" icon={<DownloadOutlined rev={undefined} />} />
            </a>
          ) : (
            <></>
          )}
        </>
      ),
    },
  ];

  const dataSource = props.value.map((t, i) => ({
    ...t,
    tetrad_polarity: props.tetradPolarities?.[i] || "",
  }));

  return (
    <>
      <h2 id={props.id ? "tetrads" : ""} style={{ marginTop: "40px" }}>
        Tetrads
      </h2>
      <Table
        style={{ textAlign: "center" }}
        dataSource={dataSource}
        columns={columns_tetrad}
        scroll={
          !context.viewSettings.isCompressedViewNeeded
            ? { x: "auto" }
            : { x: "100%" }
        }
        rowClassName={(_r, i) =>
          dataSource[i].sequence == "GGGG" && props.g4Limited
            ? "colored-row"
            : ""
        }
      />
      <div className="horizontal-center">
        {JsonToCsvButton(dataSource, ['number', 'sequence', 'name', 'onz_class', 'gbaClassification', 'planarity', 'tetrad_polarity'], ['Number', 'Sequence', 'Sequence (full names)', 'ONZ class', 'Tetrad combination', 'Planarity [Å]', 'Tetrad polarity'], 'tetrad_results')}
      </div>
    </>
  );
}
