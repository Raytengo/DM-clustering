import React, { useState, useEffect } from 'react';
import './App.css';
import ClusterVisualization from './components/ClusterVisualization';
import InputForm from './components/InputForm';
import ClusterInfo from './components/ClusterInfo';
import MetricsComparison from './components/MetricsComparison';

function App() {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('agglomerative');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [clusters, setClusters] = useState({});
  const [visualizationData, setVisualizationData] = useState(null);
  const [features, setFeatures] = useState({});
  const [error, setError] = useState(null);

  const API_URL = 'http://localhost:5001/api';

  // Fetch features on mount
  useEffect(() => {
    fetchFeatures();
    fetchClusters();
  }, []);

  // Fetch new clusters when algorithm changes
  useEffect(() => {
    fetchClusters();
    fetchVisualization();
  }, [selectedAlgorithm]);

  const fetchFeatures = async () => {
    try {
      const response = await fetch(`${API_URL}/features`);
      const data = await response.json();
      
      // Fetch data summary for default values
      const summaryResponse = await fetch(`${API_URL}/data-summary`);
      const summary = await summaryResponse.json();
      
      setFeatures(summary);
      setError(null);
    } catch (err) {
      setError('Failed to load features: ' + err.message);
    }
  };

  const fetchClusters = async () => {
    try {
      const response = await fetch(`${API_URL}/clusters?algorithm=${selectedAlgorithm}`);
      const data = await response.json();
      setClusters(data);
      setError(null);
    } catch (err) {
      setError('Failed to load clusters: ' + err.message);
    }
  };

  const fetchVisualization = async () => {
    try {
      const response = await fetch(`${API_URL}/visualize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm: selectedAlgorithm })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data.points || data.points.length === 0) {
        throw new Error('No visualization data received');
      }
      
      setVisualizationData(data);
      setError(null);
    } catch (err) {
      console.error('Visualization fetch error:', err);
      setError('Failed to load visualization: ' + err.message);
    }
  };

  const handlePredict = async (inputData) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...inputData,
          algorithm: selectedAlgorithm
        })
      });
      
      if (!response.ok) {
        throw new Error('Prediction failed');
      }
      
      const data = await response.json();
      setPrediction(data);
      setError(null);
    } catch (err) {
      setError('Prediction error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎯 Clustering Analysis Dashboard</h1>
        <p>Interactive Mall Customer Clustering Visualization</p>
      </header>

      <div className="container">
        {error && <div className="error-message">{error}</div>}

        <div className="algorithm-selector">
          <label htmlFor="algorithm">Select Algorithm:</label>
          <select 
            id="algorithm"
            value={selectedAlgorithm} 
            onChange={(e) => setSelectedAlgorithm(e.target.value)}
            className="algorithm-select"
          >
            <option value="agglomerative">Agglomerative Clustering</option>
            <option value="divisive">Divisive Clustering</option>
            <option value="dbscan">DBSCAN</option>
          </select>
        </div>

        <div className="main-grid">
          {/* Left Column: Input Form */}
          <div className="left-column">
            <div className="card">
              <h2>📝 Enter Your Data</h2>
              <InputForm 
                onSubmit={handlePredict}
                loading={loading}
                features={features}
              />
            </div>

            {prediction && (
              <div className="card prediction-result">
                <h2>✨ Your Cluster</h2>
                <ClusterInfo 
                  prediction={prediction}
                  clusterName={getClusterName(prediction.predicted_cluster)}
                />
              </div>
            )}
          </div>

          {/* Right Column: Visualization */}
          <div className="right-column">
            <div className="card">
              <h2>📊 Cluster Visualization</h2>
              {visualizationData && (
                <ClusterVisualization 
                  data={visualizationData}
                  prediction={prediction}
                  algorithmName={getAlgorithmName(selectedAlgorithm)}
                />
              )}
              {!visualizationData && <p className="loading">Loading visualization...</p>}
            </div>

            <div className="card">
              <h2>📈 Cluster Summary</h2>
              {clusters.clusters && (
                <MetricsComparison clusters={clusters.clusters} />
              )}
            </div>
          </div>
        </div>
      </div>

      <footer className="app-footer">
        <p>Data Mining Project | Clustering Analysis 2024</p>
      </footer>
    </div>
  );
}

function getAlgorithmName(algo) {
  const names = {
    agglomerative: 'Agglomerative Clustering',
    divisive: 'Divisive Clustering',
    dbscan: 'DBSCAN'
  };
  return names[algo] || algo;
}

function getClusterName(clusterId) {
  const names = {
    0: 'High-Value Customers',
    1: 'Standard Customers',
    2: 'Budget Spenders',
    3: 'Affluent but Cautious',
    4: 'Low-Engagement Customers'
  };
  return names[clusterId] || `Cluster ${clusterId}`;
}

export default App;
