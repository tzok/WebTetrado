import { Button, Image, Radio, Switch, Tooltip } from "antd";
import config from "../../config.json";
import { DownloadOutlined } from "@ant-design/icons";
import { quadruplex, result_values } from "../../types/RestultSet";
import { MolStarWrapper } from "../molstar/MolStarWrapper";
import { VisualisationLegend } from "./Legend";
import { visualsation_switch_result } from "../../types/RestultSet";
import { Suspense, useState } from "react";
import { RenderLoader } from "./RenderLoader";

function downloadFile(type: any, url: any) {
  const requestOptions = {
    method: "GET",
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  };
  fetch(url, requestOptions)
    .then((res) => res.blob())
    .then((blob) => {
      let url = URL.createObjectURL(blob);
      let pom = document.createElement("a");
      pom.setAttribute("href", url);
      pom.setAttribute("download", type);
      pom.click();
    });
}
function varna_url(
  resultSet: result_values,
  visualisationSwitchOptions: visualsation_switch_result
) {
  if (visualisationSwitchOptions.varna_can) {
    if (visualisationSwitchOptions.varna_non_can) {
      return config.SERVER_URL + resultSet.varna_can_non_can;
    } else {
      return config.SERVER_URL + resultSet.varna_can;
    }
  } else {
    if (visualisationSwitchOptions.varna_non_can) {
      return config.SERVER_URL + resultSet.varna_non_can;
    } else {
      return config.SERVER_URL + resultSet.varna;
    }
  }
}
function r_chie_url(
  resultSet: result_values,
  visualisationSwitchOptions: visualsation_switch_result
) {
  if (visualisationSwitchOptions.r_chie_canonical) {
    return config.SERVER_URL + resultSet.r_chie_canonical;
  } else {
    return config.SERVER_URL + resultSet.r_chie;
  }
}

interface StructureVisualisationArguments {
  value: quadruplex;
  resultSet: result_values;
  id: boolean;
}

export default function StructureVisualisation(
  props: StructureVisualisationArguments
) {

  const extension = props.resultSet.structure_file.split(".").splice(-1)[0];
  let visualisation_switch: visualsation_switch_result = {
    varna_non_can: false,
    varna_can: false,
    r_chie_canonical: false,
  };
  let [visualisationSwitchOptions, setSwitchOptions] =
    useState(visualisation_switch);
  let [representationMolStar, setRepresentationMolStar] = useState<string>("cartoon")
  return (
    <div id={props.id ? "result-visualization" : ""}>
      <div>

        <VisualisationLegend />
        <br />
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            flexWrap: "wrap",
          }}
        >
          <div
            hidden={props.resultSet.varna == ""}
            className="result-visualization"
          >
            <h2>
              Classic diagram (by{" "}
              <a target={"_blank"} href="/help#secondary_drawing_varna">
                VARNA
              </a>)
            </h2>
            <div
              style={{ padding: "20px", flexDirection: "column" }}
              className={"vertical-center"}
            >
              <Tooltip
                title={
                  props.resultSet.varna_can == ""
                    ? "The analyzed quadruplex does not have any canonical base pairs outside of tetrads"
                    : ""
                }
              >
                <div
                  style={{ paddingBottom: "10px" }}
                  className="horizontal-item-center"
                >
                  <div className="item-label">
                    Show canonical base pairs outside tetrads:
                  </div>
                  <Switch
                    checked={visualisationSwitchOptions.varna_can}
                    checkedChildren="Yes"
                    unCheckedChildren="No"
                    disabled={props.resultSet.varna_can == ""}
                    onChange={() =>
                      setSwitchOptions({
                        ...visualisationSwitchOptions,
                        varna_can: !visualisationSwitchOptions.varna_can,
                      })
                    }
                  />
                </div>
              </Tooltip>
              <Tooltip
                title={
                  props.resultSet.varna_non_can == ""
                    ? "The analyzed quadruplex does not have any non-canonical base pairs outside of tetrads"
                    : ""
                }
              >
                <div
                  style={{ paddingBottom: "10px" }}
                  className="horizontal-item-center"
                >
                  <div className="item-label">
                    Show non-canonical base pairs outside tetrads:
                  </div>
                  <Switch
                    checked={visualisationSwitchOptions.varna_non_can}
                    checkedChildren="Yes"
                    unCheckedChildren="No"
                    disabled={props.resultSet.varna_non_can == ""}
                    onChange={() =>
                      setSwitchOptions({
                        ...visualisationSwitchOptions,
                        varna_non_can: !visualisationSwitchOptions.varna_non_can,
                      })
                    }
                  />
                </div>
              </Tooltip>
              <Image
                alt={"varna"}
                className="two-d-image"
                src={varna_url(props.resultSet, visualisationSwitchOptions)}
              />
              <br />
              <Button
                type="primary"
                shape="round"
                icon={<DownloadOutlined rev={undefined} />}
                style={{ marginTop: "15px" }}
                size={"large"}
                onClick={() => {
                  if (
                    visualisationSwitchOptions.varna_non_can &&
                    visualisationSwitchOptions.varna_can
                  ) {
                    downloadFile(
                      "varna_canonical_and_non_canonical.svg",
                      varna_url(props.resultSet, visualisationSwitchOptions)
                    );
                  }
                  if (
                    !visualisationSwitchOptions.varna_non_can &&
                    visualisationSwitchOptions.varna_can
                  ) {
                    downloadFile(
                      "varna_canonical.svg",
                      varna_url(props.resultSet, visualisationSwitchOptions)
                    );
                  }
                  if (
                    visualisationSwitchOptions.varna_non_can &&
                    !visualisationSwitchOptions.varna_can
                  ) {
                    downloadFile(
                      "varna_non_canonical.svg",
                      varna_url(props.resultSet, visualisationSwitchOptions)
                    );
                  }
                  if (
                    !visualisationSwitchOptions.varna_non_can &&
                    !visualisationSwitchOptions.varna_can
                  ) {
                    downloadFile(
                      "varna.svg",
                      varna_url(props.resultSet, visualisationSwitchOptions)
                    );
                  }
                }}
              >
                Download
              </Button>
            </div>
          </div>
          <div
            hidden={props.resultSet.r_chie == ""}
            className="result-visualization"
          >
            <h2>
              Arc diagram (by{" "}
              <a target={"_blank"} href="/help#secondary_drawing_rchie">
                R-chie
              </a>
              )
            </h2>
            <div
              style={{ padding: "20px", flexDirection: "column" }}
              className={"vertical-center"}
            >
              <Tooltip
                title={
                  props.resultSet.r_chie_canonical == ""
                    ? "The analyzed quadruplex does not have any canonical base pairs outside of tetrads"
                    : ""
                }
              >
                <div className="horizontal-item-center">
                  <div className="item-label">
                    Show canonical base pairs outside tetrads:{" "}
                  </div>
                  <Switch
                    checked={visualisationSwitchOptions.r_chie_canonical}
                    checkedChildren="Yes"
                    unCheckedChildren="No"
                    disabled={props.resultSet.r_chie_canonical == ""}
                    onChange={() =>
                      setSwitchOptions({
                        ...visualisationSwitchOptions,
                        r_chie_canonical:
                          !visualisationSwitchOptions.r_chie_canonical,
                      })
                    }
                  />
                </div>
              </Tooltip>
              <div style={{ marginTop: "64px" }}></div>
              <Image
                alt="r-chie"
                className="two-d-image"
                src={r_chie_url(props.resultSet, visualisationSwitchOptions)}
              />
              <br />
              <Button
                type="primary"
                shape="round"
                icon={<DownloadOutlined rev={undefined} />}
                style={{ marginTop: "15px" }}
                size={"large"}
                onClick={() => {
                  downloadFile(
                    "r_chie.svg",
                    config.SERVER_URL + props.resultSet.r_chie
                  );
                  if (!visualisationSwitchOptions.r_chie_canonical) {
                    downloadFile(
                      "r_chie.svg",
                      r_chie_url(props.resultSet, visualisationSwitchOptions)
                    );
                  }
                  if (visualisationSwitchOptions.r_chie_canonical) {
                    downloadFile(
                      "r_chie_canonical.svg",
                      r_chie_url(props.resultSet, visualisationSwitchOptions)
                    );
                  }
                }}
              >
                Download
              </Button>
            </div>
          </div>
          <div
            hidden={props.resultSet.draw_tetrado == ""}
            className="result-visualization"
          >
            <h2>Layer diagram (by{" "}
              <a target={"_blank"} href="/help#secondary_drawing_drawtetrado">
                DrawTetrado
              </a>
              )</h2>
            <div
              style={{ padding: "20px", flexDirection: "column" }}
              className={"vertical-center"}
            >
              <div style={{ marginTop: "108px" }}></div>
              <Image
                alt="draw-tetrado"
                className="two-d-image"
                src={config.SERVER_URL + props.resultSet.draw_tetrado}
              />
              <br />

              <Button
                type="primary"
                shape="round"
                icon={<DownloadOutlined rev={undefined} />}
                style={{ marginTop: "15px" }}
                size={"large"}
                onClick={() =>
                  downloadFile(
                    "drawTetrado.svg",
                    config.SERVER_URL + props.resultSet.draw_tetrado
                  )
                }
              >
                Download
              </Button>
            </div>
          </div>
        </div>
        <div style={{ display: "block", marginTop: "50px" }}>
          {props.resultSet.structure_file != "" ? (
            <div>
              <h2>3D structure (by{" "}
                <a target={"_blank"} href="https://molstar.org" rel="noreferrer"
                >
                  Mol*
                </a>
                )</h2>
              <Suspense fallback={<RenderLoader />}>
                <MolStarWrapper
                  structure_file={
                    config.SERVER_URL + props.resultSet.structure_file
                  }
                  tetrads={props.value.tetrad}
                  representation={representationMolStar}
                />
              </Suspense>
              <br />

              <div className="horizontal-center" style={{ width: "100%" }}>
                <div className="vertical-center">
                  <div>
                    <Radio.Group options={[
                      { label: 'Show as cartoon', value: 'cartoon' },
                      { label: 'Show as balls and sticks', value: 'ball-and-stick' },
                    ]} onChange={(v) => { setRepresentationMolStar(v.target.value); }} value={representationMolStar} optionType="button" />
                  </div>
                  <div>
                    <Button
                      type="primary"
                      shape="round"
                      icon={<DownloadOutlined rev={undefined} />}
                      style={{ marginTop: "15px" }}
                      size={"large"}
                      onClick={() =>
                        downloadFile(
                          "structure." + extension,
                          config.SERVER_URL + props.resultSet.structure_file
                        )
                      }
                    >
                      Download
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <></>
          )}
        </div>
      </div>
    </div >
  );
}
