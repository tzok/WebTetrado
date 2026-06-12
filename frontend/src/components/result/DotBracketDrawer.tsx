import { Tooltip } from "antd";
import { useEffect, useState } from "react";
import {
  ONZ_COLORS_STRING,
  ONZ_TEXTS_COLOR_STRING,
  STRING_ONZ_COLORS,
} from "../../assets/data/onzClassColor";
import {
  dot_bracket_values,
  helice,
  nucleotide,
  quadruplex,
  quadruplex_dot_bracket_values,
  tetrad,
} from "../../types/RestultSet";

interface DotBracketDrawerArguments {
  helice: helice[];
  nucleotides: nucleotide[];
  dot_bracket: dot_bracket_values;
  quadruplex_dot_bracket?: quadruplex_dot_bracket_values;
}

const DotBracketDrawer = (props: DotBracketDrawerArguments) => {
  let [bracketArray, setBracketArray] = useState<Map<number, string>>(
    new Map<number, string>()
  );
  useEffect(() => {
    let onz_bracket_map = new Map<number, string>();
    props.helice.forEach((helice: helice) => {
      helice.quadruplexes.forEach((quadruplex: quadruplex) => {
        quadruplex.tetrad.forEach((tetrad: tetrad) => {
          tetrad.name.split("-").forEach((nucleotide: string) => {
            onz_bracket_map.set(
              props.nucleotides[
                props.nucleotides.findIndex((value: any) => {
                  return value.name == nucleotide;
                })
              ].number,
              ONZ_COLORS_STRING[tetrad.onz_class]
            );
          });
        });
      });
    });
    setBracketArray(onz_bracket_map);
  }, []);

  const renderLine = (line: string, prefix: string) => {
    return line.split("").map((sequence: string, index: number) =>
      sequence == "-" ? (
        <span
          style={{ fontFamily: '"PT Mono", monospace' }}
          key={prefix + index.toString()}
        >
          {sequence}
        </span>
      ) : bracketArray?.has(
          index +
            1 -
            (props.dot_bracket.sequence.slice(0, index).match(/-/g) || [])
              .length
        ) ? (
        <Tooltip
          key={prefix + index.toString()}
          placement="top"
          title={
            STRING_ONZ_COLORS[
              bracketArray?.get(
                index +
                  1 -
                  (
                    props.dot_bracket.sequence
                      .slice(0, index)
                      .match(/-/g) || []
                  ).length
              ) || ""
            ]
          }
        >
          <span
            style={{
              fontFamily: '"PT Mono", monospace',
              backgroundColor: bracketArray?.get(
                index +
                  1 -
                  (
                    props.dot_bracket.sequence
                      .slice(0, index)
                      .match(/-/g) || []
                  ).length
              ),
              color:
                ONZ_TEXTS_COLOR_STRING[
                  STRING_ONZ_COLORS[
                    bracketArray?.get(
                      index +
                        1 -
                        (
                          props.dot_bracket.sequence
                            .slice(0, index)
                            .match(/-/g) || []
                        ).length
                    )!
                  ]
                ],
            }}
          >
            {sequence}
          </span>
        </Tooltip>
      ) : (
        <span
          style={{ fontFamily: '"PT Mono", monospace' }}
          key={prefix + index.toString()}
        >
          {sequence}
        </span>
      )
    );
  };

  return (
    <>
      <p
        style={{
          whiteSpace: "pre-wrap",
          fontSize: "20px",
          marginLeft: "10px",
          fontFamily: "'PT Mono', monospace",
        }}
      >
        {renderLine(props.dot_bracket.sequence, "dbs")}
        <br />
        {renderLine(props.dot_bracket.line1, "dbl1")}
        <br />
        {renderLine(props.dot_bracket.line2, "dbl2")}
        <br />
      </p>
      {props.quadruplex_dot_bracket &&
       props.quadruplex_dot_bracket.sequence && (
        <>
          <h3 style={{ marginLeft: "10px", marginTop: "20px" }}>
            Quadruplex dot-bracket
          </h3>
          <p
            style={{
              whiteSpace: "pre-wrap",
              fontSize: "20px",
              marginLeft: "10px",
              fontFamily: "'PT Mono', monospace",
            }}
          >
            {renderLine(props.quadruplex_dot_bracket.sequence, "qdb_seq")}
            <br />
            {renderLine(props.quadruplex_dot_bracket.structure, "qdb_str")}
            <br />
            {renderLine(props.quadruplex_dot_bracket.chi, "qdb_chi")}
            <br />
            {renderLine(props.quadruplex_dot_bracket.sugar, "qdb_sugar")}
            <br />
            {renderLine(props.quadruplex_dot_bracket.loop, "qdb_loop")}
            <br />
          </p>
        </>
      )}
    </>
  );
};

export default DotBracketDrawer;
