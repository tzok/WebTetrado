import { Steps, Tabs, Alert, message, Tooltip } from "antd";
import { useParams } from "react-router-dom";
import { lazy, Suspense, useEffect, useState } from "react";
import { result_values } from "../../types/RestultSet";
import { processingResponse } from "../../utils/adapters/processingResponse";
import { Divider } from "../layout/common/Divider";
import { RenderLoader } from "./RenderLoader";
import DotBracketDrawer from "./DotBracketDrawer";
import ResultDescription from "./ResultDescription";
import WebPushSubscriptionButton from "./WebPushSubscriptionButton";
import crying_rna from "../../assets/images/crying_rna.png";

const TetradTable = lazy(() => import("./TetradTable"));
const LoopTable = lazy(() => import("./LoopTable"));
const ChiAngleTable = lazy(() => import("./ChiAngleTable"));
const TetradPairTable = lazy(() => import("./TetradPairTable"));
const BasePairTable = lazy(() => import("./BasePairTable"));
const NucleotideTable = lazy(() => import("./NucleotideTable"));
const StructureVisualisation = lazy(() => import("./StructureVisualisation"));
 
export const Result = () => {
  let result: result_values = {
    analyzer: "RNApolis Annotator",
    name: "",
    dot_bracket: { line1: "", line2: "", sequence: "" },
    status: 0,
    error_message: "",
    structure_method: "",
    structure_file: "",
    varna: "",
    varna_can: "",
    varna_can_non_can: "",
    varna_non_can: "",
    r_chie: "",
    r_chie_canonical: "",
    model: 1,
    draw_tetrado: "",
    idcode: "",
    g4_limited: false,
    base_pairs: [],
    helices: [],
    nucleotides: [],
    remove_date: "",
  };


  const { requestNumber } = useParams<{ requestNumber: string }>();
  let [currentTab, setCurrentTab] = useState("00");
  let [loadingResult, setLoadingResult] = useState(true);
  let [resultSet, setResultSet] = useState(result);
  const steps = [
    { title: "Task uploaded" },
    { title: "Queueing" },
    { title: "Processing" },
    {
      title: "Task completed",
      description:
        resultSet.status === 4
          ? "Results will be stored until " + resultSet.remove_date + "."
          : "",
    },
  ];
  useEffect(() => {
    processingResponse(
      requestNumber,
      setResultSet,
      resultSet,
      setLoadingResult
    );
  }, []);

  return (
    <>
       <WebPushSubscriptionButton
        status={resultSet.status}
        requestNumber={requestNumber}
      /> 

      <h2>
        Task id:{" "}
        <span
          onClick={() => {
            window.navigator["clipboard"].writeText(requestNumber!);
            message.success("Request task id has been saved to clipboard.");
          }}
        >
          <Tooltip title="Click here to copy to clipboard.">
            <i>{requestNumber}</i>
          </Tooltip>
        </span>
      </h2>

      {resultSet.status >= 1 ? <p>Analyzer: <b>{resultSet.analyzer}</b></p> : <></>}

      <Steps current={resultSet.status} items={steps} status="wait" />
      {resultSet.status == 5 ? (
        <Alert
          message="Server error"
          showIcon
          description={resultSet.error_message}
          type="error"
          style={{ margin: "20px" }}
        />
      ) : (
        <></>
      )}
      {loadingResult ? (
        <RenderLoader />
      ) : (
        <>
          <Divider />
          {resultSet.status == 0 ?
            <div className={'horizontal-center'} style={{ width: "100%", flexDirection: 'column' }}>

              <img
                alt="Bełek by Marta Maćkowiak"
                style={{ width: "400px", marginLeft: 'auto', marginRight: 'auto', paddingRight: "36px" }}
                src={crying_rna}
              />
              <h2 style={{ paddingTop: '15px', textAlign: 'center' }}>
                No results exist in the system for task <i>{requestNumber}</i>
              </h2>

            </div> : (<>
              {
                resultSet.helices.length == 0 ? (
                  <>
                    <h2
                      id="result"
                      style={{
                        marginTop: "40px",
                        whiteSpace: "pre-wrap",
                        fontSize: "20px",
                        marginLeft: "10px",
                        fontFamily: "'PT Mono', monospace",
                      }}
                    >
                      Quadruplexes not found
                    </h2>
                  </>
                ) : (
                  <>
                    <h2
                      id="result"
                      style={{
                        marginTop: "40px",
                        whiteSpace: "pre-wrap",
                        fontSize: "20px",
                        marginLeft: "10px",
                        fontFamily: "'PT Mono', monospace",
                      }}
                    >
                      {resultSet.name}
                    </h2>
                    <Tabs
                      defaultActiveKey="0"
                      type="card"
                      tabPosition={"top"}
                      onChange={(aK) => {
                        setCurrentTab(aK + "0");
                      }}
                      items={[...Array.from(resultSet.helices, (z, i) => z)].map(
                        (z, i) => {
                          return {
                            label: `N4-Helix ${i + 1}`,
                            key: i.toString(),
                            children: (
                              <>
                                <Tabs
                                  defaultActiveKey="0"
                                  type="card"
                                  onChange={(aK) => {
                                    setCurrentTab(i.toString() + aK);
                                  }}
                                  tabPosition={"top"}
                                  items={[
                                    ...Array.from(
                                      resultSet.helices[i].quadruplexes,
                                      (v, j) => v
                                    ),
                                  ].map((v, j) => {
                                    return {
                                      label: `Quadruplex ${j + 1}`,
                                      key: j.toString(),
                                      children: (
                                        <>
                                          <ResultDescription
                                            resultSet={resultSet}
                                            quadruplex={v}
                                          />
                                          <Divider />
                                          <h2
                                            id={
                                              currentTab == i.toString() + j.toString()
                                                ? "two-d-structure"
                                                : ""
                                            }
                                            style={{ marginTop: "40px" }}
                                          >
                                            2D structure (dot-bracket):
                                          </h2>
                                          <DotBracketDrawer
                                            helice={resultSet.helices}
                                            nucleotides={resultSet.nucleotides}
                                            dot_bracket={resultSet.dot_bracket}
                                          />
                                          <Suspense fallback={<RenderLoader />}>
                                            <StructureVisualisation
                                              value={v}
                                              resultSet={resultSet}
                                              id={
                                                currentTab ==
                                                i.toString() + j.toString()
                                              }
                                            />
                                          </Suspense>
                                          <Divider />
                                          <Suspense fallback={<RenderLoader />}>
                                            <TetradTable
                                              value={v.tetrad}
                                              g4Limited={resultSet.g4_limited}
                                              id={
                                                currentTab ==
                                                i.toString() + j.toString()
                                              }
                                            />
                                          </Suspense>
                                          <Divider />
                                          <Suspense fallback={<RenderLoader />}>
                                            <LoopTable
                                              value={v.loop}
                                              id={
                                                currentTab ==
                                                i.toString() + j.toString()
                                              }
                                            />
                                          </Suspense>
                                          <Divider />
                                          <Suspense fallback={<RenderLoader />}>
                                            <ChiAngleTable
                                              value={v.chi_angle_value}
                                              id={
                                                currentTab ==
                                                i.toString() + j.toString()
                                              }
                                            />
                                          </Suspense>
                                        </>
                                      ),
                                    };
                                  })}
                                />
                                <Divider />
                                <Suspense fallback={<RenderLoader />}>
                                  <TetradPairTable
                                    value={z.tetrad_pairs}
                                    id={currentTab.startsWith(i.toString())}
                                  />
                                </Suspense>
                                <Divider />
                                <Suspense fallback={<RenderLoader />}>
                                  <BasePairTable
                                    value={resultSet.base_pairs}
                                    id={currentTab.startsWith(i.toString())}
                                  />
                                </Suspense>
                                <Divider />
                                <Suspense fallback={<RenderLoader />}>
                                  <NucleotideTable
                                    value={resultSet.nucleotides}
                                    id={currentTab.startsWith(i.toString())}
                                  />
                                </Suspense>
                              </>
                            ),
                          };
                        }
                      )}
                    />
                  </>
                )
              }</>)}
        </>
      )}
    </>
  )
};
