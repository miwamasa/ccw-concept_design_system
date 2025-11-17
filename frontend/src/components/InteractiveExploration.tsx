import React, { useState } from 'react';
import { GraphVisualization } from './GraphVisualization';
import {
  startInteractiveExploration,
  assessSituation,
  identifyProblem,
  establishIntention,
  decomposeIntention,
  applySolution,
  ExplorationState,
} from '../services/api';
import './InteractiveExploration.css';

export const InteractiveExploration: React.FC = () => {
  const [explorationState, setExplorationState] = useState<ExplorationState | null>(null);
  const [initialSystem, setInitialSystem] = useState('car_running');
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // For decomposition
  const [subIntentions, setSubIntentions] = useState<string[]>(['']);
  const [subSystems, setSubSystems] = useState<string[]>(['']);

  const handleStart = async () => {
    setLoading(true);
    setError(null);
    try {
      const state = await startInteractiveExploration(initialSystem);
      setExplorationState(state);
      setInputValue(state.suggested_situation || '');
    } catch (err) {
      setError('Failed to start exploration: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleSituation = async () => {
    setLoading(true);
    setError(null);
    try {
      const state = await assessSituation(inputValue);
      setExplorationState(state);
      setInputValue(state.suggested_problem || '');
    } catch (err) {
      setError('Failed to assess situation: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleProblem = async () => {
    setLoading(true);
    setError(null);
    try {
      const state = await identifyProblem(inputValue);
      setExplorationState(state);
      setInputValue(state.suggested_intention || '');
    } catch (err) {
      setError('Failed to identify problem: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleIntention = async () => {
    setLoading(true);
    setError(null);
    try {
      const state = await establishIntention(inputValue);
      setExplorationState(state);
      setInputValue('');

      // Pre-fill decomposition if available
      if (state.suggested_decomposition) {
        setSubIntentions(state.suggested_decomposition.intentions);
        setSubSystems(state.suggested_decomposition.systems);
      }
    } catch (err) {
      setError('Failed to establish intention: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleDecompose = async () => {
    setLoading(true);
    setError(null);
    try {
      const state = await decomposeIntention(
        subIntentions.filter(s => s.trim() !== ''),
        subSystems.filter(s => s.trim() !== '')
      );
      setExplorationState(state);
      setInputValue(state.suggested_situation || '');
      setSubIntentions(['']);
      setSubSystems(['']);
    } catch (err) {
      setError('Failed to decompose intention: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleSolution = async (solution: string) => {
    setLoading(true);
    setError(null);
    try {
      const state = await applySolution(solution);
      setExplorationState(state);
      setInputValue(state.suggested_situation || '');
    } catch (err) {
      setError('Failed to apply solution: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = () => {
    if (!explorationState) return null;

    switch (explorationState.step) {
      case 'situation_assessment':
        return (
          <div className="step-content">
            <h3>Step: Situation Assessment (SI Component)</h3>
            <p className="step-message">{explorationState.message}</p>
            <p><strong>System:</strong> {explorationState.system}</p>

            <div className="input-section">
              <label>Enter Situation:</label>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="e.g., obstacle_detected"
              />
              <button onClick={handleSituation} disabled={loading || !inputValue.trim()}>
                Assess Situation
              </button>
            </div>

            {explorationState.available_situations && explorationState.available_situations.length > 0 && (
              <div className="suggestions">
                <strong>Available situations:</strong>
                <div className="suggestion-chips">
                  {explorationState.available_situations.map((s, i) => (
                    <span key={i} className="chip" onClick={() => setInputValue(s)}>
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 'problem_identification':
        return (
          <div className="step-content">
            <h3>Step: Problem Identification (PI Component)</h3>
            <p className="step-message">{explorationState.message}</p>
            <p><strong>Situation:</strong> {explorationState.situation}</p>

            <div className="input-section">
              <label>Enter Problem:</label>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="e.g., collision_risk"
              />
              <button onClick={handleProblem} disabled={loading || !inputValue.trim()}>
                Identify Problem
              </button>
            </div>

            {explorationState.available_problems && explorationState.available_problems.length > 0 && (
              <div className="suggestions">
                <strong>Available problems:</strong>
                <div className="suggestion-chips">
                  {explorationState.available_problems.map((p, i) => (
                    <span key={i} className="chip" onClick={() => setInputValue(p)}>
                      {p}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 'establish_intention':
        return (
          <div className="step-content">
            <h3>Step: Establish Intention (EI Component)</h3>
            <p className="step-message">{explorationState.message}</p>
            <p><strong>Problem:</strong> {explorationState.problem}</p>

            <div className="input-section">
              <label>Enter Intention:</label>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="e.g., avoid_collision"
              />
              <button onClick={handleIntention} disabled={loading || !inputValue.trim()}>
                Establish Intention
              </button>
            </div>

            {explorationState.available_intentions && explorationState.available_intentions.length > 0 && (
              <div className="suggestions">
                <strong>Available intentions:</strong>
                <div className="suggestion-chips">
                  {explorationState.available_intentions.map((i, idx) => (
                    <span key={idx} className="chip" onClick={() => setInputValue(i)}>
                      {i}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 'choose_path':
        return (
          <div className="step-content">
            <h3>Step: Choose Path</h3>
            <p className="step-message">{explorationState.message}</p>
            <p><strong>Intention:</strong> {explorationState.intention}</p>

            <div className="choice-buttons">
              {explorationState.can_decompose && (
                <div className="decompose-section">
                  <h4>Decompose Intention (DI Component)</h4>
                  <div className="decompose-inputs">
                    <div className="input-list">
                      <label>Sub-intentions:</label>
                      {subIntentions.map((intent, idx) => (
                        <input
                          key={idx}
                          type="text"
                          value={intent}
                          onChange={(e) => {
                            const newIntents = [...subIntentions];
                            newIntents[idx] = e.target.value;
                            setSubIntentions(newIntents);
                          }}
                          placeholder={`Sub-intention ${idx + 1}`}
                        />
                      ))}
                      <button onClick={() => setSubIntentions([...subIntentions, ''])}>
                        + Add Sub-intention
                      </button>
                    </div>

                    <div className="input-list">
                      <label>Sub-systems:</label>
                      {subSystems.map((sys, idx) => (
                        <input
                          key={idx}
                          type="text"
                          value={sys}
                          onChange={(e) => {
                            const newSystems = [...subSystems];
                            newSystems[idx] = e.target.value;
                            setSubSystems(newSystems);
                          }}
                          placeholder={`Sub-system ${idx + 1}`}
                        />
                      ))}
                      <button onClick={() => setSubSystems([...subSystems, ''])}>
                        + Add Sub-system
                      </button>
                    </div>
                  </div>
                  <button
                    className="action-button primary"
                    onClick={handleDecompose}
                    disabled={loading || subIntentions.filter(s => s.trim()).length === 0}
                  >
                    Decompose Intention
                  </button>
                </div>
              )}

              {explorationState.can_apply_solution && explorationState.available_solutions && (
                <div className="solution-section">
                  <h4>Apply Solution (SA Component)</h4>
                  <p>Choose a solution to apply:</p>
                  <div className="solution-buttons">
                    {explorationState.available_solutions.map((sol, idx) => (
                      <button
                        key={idx}
                        className="action-button"
                        onClick={() => handleSolution(sol)}
                        disabled={loading}
                      >
                        {sol}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        );

      case 'completed':
        return (
          <div className="step-content completed">
            <h3>✓ Design Exploration Completed!</h3>
            <p>{explorationState.message}</p>
            <button onClick={() => {
              setExplorationState(null);
              setInputValue('');
              setSubIntentions(['']);
              setSubSystems(['']);
            }}>
              Start New Exploration
            </button>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="interactive-exploration">
      <div className="exploration-header">
        <h2>Interactive Design Exploration</h2>
        <p>Step-by-step design exploration using DE components</p>
      </div>

      {!explorationState ? (
        <div className="start-section">
          <h3>Start New Exploration</h3>
          <div className="input-group">
            <label>Initial System:</label>
            <input
              type="text"
              value={initialSystem}
              onChange={(e) => setInitialSystem(e.target.value)}
              placeholder="e.g., car_running"
            />
          </div>
          <button
            className="start-button"
            onClick={handleStart}
            disabled={loading || !initialSystem.trim()}
          >
            {loading ? 'Starting...' : 'Start Exploration'}
          </button>

          <div className="info-box">
            <h4>Example Scenario: Collision Avoidance System</h4>
            <p>Try starting with: <strong>car_running</strong></p>
            <p>The system will guide you through:</p>
            <ul>
              <li>Situation Assessment (SI)</li>
              <li>Problem Identification (PI)</li>
              <li>Establish Intention (EI)</li>
              <li>Decompose Intention (DI) or Apply Solution (SA)</li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="exploration-progress">
          {renderStepContent()}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {explorationState.pending_subsystems && explorationState.pending_subsystems.length > 0 && (
            <div className="pending-info">
              <strong>Pending subsystems to explore:</strong>
              <ul>
                {explorationState.pending_subsystems.map((sys, idx) => (
                  <li key={idx}>{sys}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {explorationState && (
        <div className="graph-display">
          <GraphVisualization
            graphData={explorationState.graph}
            title="DE Graph (Design Exploration History)"
          />
        </div>
      )}
    </div>
  );
};
