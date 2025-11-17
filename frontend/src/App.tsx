import React, { useState } from 'react';
import { GraphVisualization } from './components/GraphVisualization';
import { exploreDesign, convertGraphs } from './services/api';
import { GraphData } from './types';
import './App.css';

function App() {
  const [initialSystem, setInitialSystem] = useState('car_running');
  const [deGraph, setDeGraph] = useState<GraphData | null>(null);
  const [ldGraph, setLdGraph] = useState<GraphData | null>(null);
  const [siGraph, setSiGraph] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExplore = async () => {
    setLoading(true);
    setError(null);

    try {
      const deData = await exploreDesign(initialSystem);
      setDeGraph(deData);
    } catch (err) {
      setError('Failed to explore design: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleConvert = async () => {
    setLoading(true);
    setError(null);

    try {
      const graphs = await convertGraphs();
      setDeGraph(graphs.de);
      setLdGraph(graphs.ld);
      setSiGraph(graphs.si);
    } catch (err) {
      setError('Failed to convert graphs: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Concept Design Support System</h1>
        <p>Component-based Concept Design Visualization</p>
      </header>

      <div className="container">
        <div className="control-panel">
          <h2>Design Exploration</h2>

          <div className="input-group">
            <label htmlFor="initial-system">Initial System:</label>
            <input
              id="initial-system"
              type="text"
              value={initialSystem}
              onChange={(e) => setInitialSystem(e.target.value)}
              placeholder="e.g., car_running"
            />
          </div>

          <div className="button-group">
            <button onClick={handleExplore} disabled={loading}>
              {loading ? 'Exploring...' : 'Start Exploration'}
            </button>
            <button onClick={handleConvert} disabled={loading || !deGraph}>
              {loading ? 'Converting...' : 'Convert to LD & SI'}
            </button>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="info-panel">
            <h3>Instructions</h3>
            <ol>
              <li>Enter an initial system (e.g., "car_running")</li>
              <li>Click "Start Exploration" to create a DE graph</li>
              <li>Click "Convert to LD & SI" to see all graph transformations</li>
            </ol>

            <h3>Graph Types</h3>
            <ul>
              <li><strong>DE Graph:</strong> Design Exploration - records design history</li>
              <li><strong>LD Graph:</strong> Logical Dependency - logical relationships</li>
              <li><strong>SI Graph:</strong> Systems Integration - final system hierarchy</li>
            </ul>
          </div>
        </div>

        <div className="graphs-panel">
          {deGraph && (
            <div className="graph-container">
              <GraphVisualization
                graphData={deGraph}
                title="DE Graph (Design Exploration)"
              />
            </div>
          )}

          {ldGraph && (
            <div className="graph-container">
              <GraphVisualization
                graphData={ldGraph}
                title="LD Graph (Logical Dependency)"
              />
            </div>
          )}

          {siGraph && (
            <div className="graph-container">
              <GraphVisualization
                graphData={siGraph}
                title="SI Graph (Systems Integration)"
              />
            </div>
          )}

          {!deGraph && !ldGraph && !siGraph && (
            <div className="empty-state">
              <h3>No graphs to display</h3>
              <p>Start a design exploration to visualize the concept design process</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
