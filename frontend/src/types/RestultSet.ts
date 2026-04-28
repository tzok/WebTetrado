export type base_pair = {
  number: number;
  edge3: string;
  edge5: string;
  nt1: string;
  nt2: string;
  stericity: string;
};

export type chi_angle_value = {
  number: number;
  nt1: string;
  nt2: string;
  nt3: string;
  nt4: string;
};

export type tetrad = {
  number: number;
  name: string;
  sequence: string;
  nucleotides: string[];
  onz_class: string;
  gbaClassification: string;
  planarity: number;
  file: string;
};
export type loop = {
  number: number;
  short_sequence: string;
  full_sequence: string;
  type: string;
  length: number;
};
export type quadruplex = {
  number: number;
  molecule: string;
  onz_class: string;
  tetrad_combination: string;
  loopClassification: string;
  structure_dot_bracked: string;
  tetrads_no: number;
  tetrad: tetrad[];
  chi_angle_value: chi_angle_value[];
  type: string;
  loop: loop[];
};
export type tetrad_pair = {
  number: number;
  tetrad1: string;
  tetrad2: string;
  rise: number;
  twist: number;
  strand_direction: string;
};
export type nucleotide = {
  number: number;
  symbol: string;
  name: string;
  nucleotides: string[];
  glycosidicBond: string;
  chi_angle: string;
};
export type helice = {
  quadruplexes: quadruplex[];
  tetrad_pairs: tetrad_pair[];
};
export type result_values = {
  name: string;
  dot_bracket: dot_bracket_values;
  status: number;
  error_message: string;
  structure_method: string;
  structure_file: string;
  g4_limited: boolean;
  idcode: string;
  varna: string;
  varna_can: string;
  varna_non_can: string;
  varna_can_non_can: string;
  r_chie: string;
  r_chie_canonical: string;
  draw_tetrado: string;
  base_pairs: base_pair[];
  helices: helice[];
  nucleotides: nucleotide[];
  remove_date: string;
  model: number;
};
export type dot_bracket_values = {
  line1: string;
  line2: string;
  sequence: string;
};
export type visualsation_switch_result = {
  varna_non_can: boolean;
  varna_can: boolean;
  r_chie_canonical: boolean;
};
export type request_form_values = {
  fileId: string;
  rcsbPdbId: string;
  settings: {
    reorder: boolean;
    g4Limited: boolean;
    model: number;
  };
};
