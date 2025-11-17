import axios from 'axios';
import { GraphData } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const exploreDesign = async (initialSystem: string): Promise<GraphData> => {
  const response = await api.post('/api/explore', {
    initial_system: initialSystem,
  });
  return response.data;
};

export const getDEGraph = async (): Promise<GraphData> => {
  const response = await api.get('/api/graphs/de');
  return response.data;
};

export const getLDGraph = async (): Promise<GraphData> => {
  const response = await api.get('/api/graphs/ld');
  return response.data;
};

export const getSIGraph = async (): Promise<GraphData> => {
  const response = await api.get('/api/graphs/si');
  return response.data;
};

export const convertGraphs = async (): Promise<{
  de: GraphData;
  ld: GraphData;
  si: GraphData;
}> => {
  const response = await api.post('/api/convert');
  return response.data;
};

// Interactive Exploration APIs

export interface ExplorationState {
  step: string;
  system?: string;
  situation?: string;
  problem?: string;
  intention?: string;
  pending_subsystems?: string[];
  suggested_situation?: string;
  suggested_problem?: string;
  suggested_intention?: string;
  can_decompose?: boolean;
  can_apply_solution?: boolean;
  suggested_decomposition?: {
    intentions: string[];
    systems: string[];
  };
  available_solutions?: string[];
  available_situations?: string[];
  available_problems?: string[];
  available_intentions?: string[];
  message?: string;
  graph: GraphData;
}

export const startInteractiveExploration = async (initialSystem: string): Promise<ExplorationState> => {
  const response = await api.post('/api/interactive/start', {
    initial_system: initialSystem,
  });
  return response.data;
};

export const assessSituation = async (situation: string): Promise<ExplorationState> => {
  const response = await api.post('/api/interactive/situation', {
    situation,
  });
  return response.data;
};

export const identifyProblem = async (problem: string): Promise<ExplorationState> => {
  const response = await api.post('/api/interactive/problem', {
    problem,
  });
  return response.data;
};

export const establishIntention = async (intention: string): Promise<ExplorationState> => {
  const response = await api.post('/api/interactive/intention', {
    intention,
  });
  return response.data;
};

export const decomposeIntention = async (
  subIntentions: string[],
  subSystems: string[]
): Promise<ExplorationState> => {
  const response = await api.post('/api/interactive/decompose', {
    sub_intentions: subIntentions,
    sub_systems: subSystems,
  });
  return response.data;
};

export const applySolution = async (solution: string): Promise<ExplorationState> => {
  const response = await api.post('/api/interactive/solution', {
    solution,
  });
  return response.data;
};

export const getExplorationState = async (): Promise<ExplorationState> => {
  const response = await api.get('/api/interactive/state');
  return response.data;
};

export const getKnowledgeBase = async () => {
  const response = await api.get('/api/knowledge-base');
  return response.data;
};

export const getAllSystems = async (): Promise<{ systems: string[] }> => {
  const response = await api.get('/api/knowledge-base/systems');
  return response.data;
};
