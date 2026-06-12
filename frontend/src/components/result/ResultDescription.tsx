import { quadruplex, result_values } from "../../types/RestultSet";
import { Descriptions, Image, Tooltip } from "antd";
import { InfoCircleOutlined } from "@ant-design/icons";
interface ResultDescriptionArguments {
  resultSet: result_values;
  quadruplex: quadruplex;
}

const ResultDescription = (props: ResultDescriptionArguments) => {
  return (
    <Descriptions
      title="Basic data"
      bordered
      layout="horizontal"
      labelStyle={{ fontWeight: "bold", textAlign: "left" }}
      contentStyle={{ whiteSpace: "normal" }}
      style={{ width: "100%" }}
    >
      {props.resultSet.idcode != "" ? (
        <Descriptions.Item label="PDB ID:">
          {props.resultSet.idcode}
        </Descriptions.Item>
      ) : (
        <></>
      )}

      {props.quadruplex.molecule != "" ? (
        <Descriptions.Item label="Molecule:">
          {props.quadruplex.molecule}
        </Descriptions.Item>
      ) : (
        <></>
      )}
      {props.resultSet.structure_method != "" ? (
        <Descriptions.Item label="Experimental method:">
          {props.resultSet.structure_method}
        </Descriptions.Item>
      ) : (
        <></>
      )}
      <Descriptions.Item label="Type (by no. of strands):">
        {props.quadruplex.type == "UNI" ? "unimolecular" : ""}
        {props.quadruplex.type == "BI" ? "bimolecular" : ""}
        {props.quadruplex.type == "TETRA" ? "tetramolecular" : ""}
        {props.quadruplex.type == "OTHER" ? "other" : ""}
      </Descriptions.Item>
      <Descriptions.Item label="No. of tetrads:">
        {props.quadruplex.tetrads_no}
      </Descriptions.Item>
      {props.quadruplex.onz_class != "" ? (
        <Descriptions.Item label="ONZM class:">
          {props.quadruplex.onz_class}
        </Descriptions.Item>
      ) : (
        <></>
      )}
      {props.quadruplex.handedness ? (
        <Descriptions.Item label="Handedness:">
          {props.quadruplex.handedness}
        </Descriptions.Item>
      ) : (
        <></>
      )}
      {props.quadruplex.tetrad_polarities && props.quadruplex.tetrad_polarities.length > 0 ? (
        <Descriptions.Item label="Tetrad polarities:">
          {props.quadruplex.tetrad_polarities.filter(p => p !== null).join(", ")}
        </Descriptions.Item>
      ) : (
        <></>
      )}
      {props.quadruplex.path && props.quadruplex.path.length > 0 ? (
        <Descriptions.Item label="Path:">
          {props.quadruplex.path.join(", ")}
        </Descriptions.Item>
      ) : (
        <></>
      )}
      {props.quadruplex.bulges && props.quadruplex.bulges.length > 0 ? (
        <Descriptions.Item label="Bulges:">
          {props.quadruplex.bulges.join(", ")}
        </Descriptions.Item>
      ) : (
        <></>
      )}
      {props.quadruplex.loopClassification.split(" ")[0] != "-" ? (
        <Descriptions.Item label="Loop topology:">
          <Tooltip
            title={
              <Image
                alt={props.quadruplex.loopClassification.split(" ")[0]}
                src={require("../../assets/da-silva/" +
                  props.quadruplex.loopClassification.split(" ")[0] +
                  ".svg")}
              />
            }
            color={"white"}
          >
            <u>{props.quadruplex.loopClassification}</u>
            <sup><InfoCircleOutlined rev={undefined} style={{ color: '#0272b4' }} /></sup>
          </Tooltip>
        </Descriptions.Item>
      ) : (
        <></>
      )}
      {props.quadruplex.tetrad_combination != "" ? (
        <Descriptions.Item label="Tetrad combination:">
          <>
            {props.quadruplex.tetrad_combination
              .split(", ")
              .map((value, ind, array) => {
                return (
                  <Tooltip
                    title={
                      <div
                        style={{
                          display: "flex",
                          direction: "ltr",
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            flexDirection: "column",
                          }}
                        >
                          <h3>{value}a</h3>
                          <Image
                            alt={value}
                            src={require("../../assets/da-silva/" +
                              value +
                              "a.svg")}
                          />
                        </div>
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            flexDirection: "column",
                          }}
                        >
                          <h3>{value}b</h3>
                          <Image
                            alt={value}
                            src={require("../../assets/da-silva/" +
                              value +
                              "b.svg")}
                          />
                        </div>
                      </div>
                    }
                    color={"white"}
                  >
                    <u>{value}</u>
                    <sup><InfoCircleOutlined rev={undefined} style={{ color: '#0272b4' }} /></sup>
                    {array.length - 1 > ind ? ", " : ""}
                  </Tooltip>
                );
              })}
          </>
        </Descriptions.Item>
      ) : (
        <></>
      )}
    </Descriptions>
  );
};
export default ResultDescription;
