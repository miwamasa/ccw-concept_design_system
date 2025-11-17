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
