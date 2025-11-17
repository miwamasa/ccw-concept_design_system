import React, { useCallback, useMemo, useEffect } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { GraphData, GraphNode, GraphEdge } from '../types';

interface GraphVisualizationProps {
  graphData: GraphData | null;
  title: string;
}

const getNodeColor = (type: string): string => {
  const colors: Record<string, string> = {
    // DE Components
    'SituationAssessment': '#4A90E2',
    'ProblemIdentification': '#E24A4A',
    'EstablishIntention': '#4AE290',
    'DecomposeIntention': '#E2C44A',
    'ConditionalBranch': '#9B4AE2',
    'SolutionAssignment': '#E24AC4',
    // SI Components
    'Condition': '#FF6B6B',
    'Backups': '#4ECDC4',
    'Collaboration': '#45B7D1',
    'Alternative': '#FFA07A',
    'Exclusive': '#98D8C8',
    // Default
    'default': '#CCCCCC',
  };
  return colors[type] || colors['default'];
};

const convertToReactFlowNodes = (graphNodes: GraphNode[]): Node[] => {
  return graphNodes.map((node, index) => {
    const label = node.type || node.id;
    const details = [];

    if (node.system) details.push(`System: ${node.system}`);
    if (node.situation) details.push(`Situation: ${node.situation}`);
    if (node.problem) details.push(`Problem: ${node.problem}`);
    if (node.intention) details.push(`Intention: ${node.intention}`);
    if (node.solution) details.push(`Solution: ${node.solution}`);
    if (node.subsystem) details.push(`Subsystem: ${node.subsystem}`);

    return {
      id: node.id,
      type: 'default',
      data: {
        label: (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
              {label}
            </div>
            {details.length > 0 && (
              <div style={{ fontSize: '10px', color: '#666' }}>
                {details.map((detail, i) => (
                  <div key={i}>{detail}</div>
                ))}
              </div>
            )}
          </div>
        ),
      },
      position: {
        x: (index % 3) * 250,
        y: Math.floor(index / 3) * 150,
      },
      style: {
        background: getNodeColor(node.type),
        color: '#fff',
        border: '2px solid #333',
        borderRadius: '8px',
        padding: '10px',
        minWidth: '200px',
      },
    };
  });
};

const convertToReactFlowEdges = (graphEdges: GraphEdge[]): Edge[] => {
  return graphEdges.map((edge, index) => ({
    id: `edge-${index}`,
    source: edge.source,
    target: edge.target,
    label: edge.logic || '',
    type: 'smoothstep',
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
    style: {
      stroke: '#333',
      strokeWidth: 2,
    },
  }));
};

export const GraphVisualization: React.FC<GraphVisualizationProps> = ({
  graphData,
  title,
}) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Update nodes and edges when graphData changes
  useEffect(() => {
    if (graphData) {
      const newNodes = convertToReactFlowNodes(graphData.nodes);
      const newEdges = convertToReactFlowEdges(graphData.edges);
      setNodes(newNodes);
      setEdges(newEdges);
    } else {
      setNodes([]);
      setEdges([]);
    }
  }, [graphData, setNodes, setEdges]);

  return (
    <div style={{ height: '500px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h3 style={{ margin: '10px', textAlign: 'center' }}>{title}</h3>
      <div style={{ height: 'calc(100% - 50px)' }}>
        {nodes.length > 0 ? (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            fitView
          >
            <Controls />
            <Background />
          </ReactFlow>
        ) : (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            color: '#999',
            fontSize: '14px'
          }}>
            No nodes to display yet. Start exploring to build the graph.
          </div>
        )}
      </div>
    </div>
  );
};
