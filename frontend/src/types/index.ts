export interface GraphNode {
  id: string;
  type: string;
  data?: any;
  system?: any;
  situation?: any;
  problem?: any;
  intention?: any;
  solution?: any;
  subsystem?: any;
  sub_intentions?: any[];
  sub_systems?: any[];
  subsystems?: any[];
  situations?: any[];
  primary?: any;
  backups?: any[];
  parent?: any;
  level?: number;
  metadata?: Record<string, any>;
}

export interface GraphEdge {
  source: string;
  target: string;
  logic?: string;
  metadata?: Record<string, any>;
}

export interface GraphData {
  type: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  hierarchies?: Record<string, string[]>;
}

export type GraphType = 'DE' | 'LD' | 'SI';
