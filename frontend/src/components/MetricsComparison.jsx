import React from 'react';
import './MetricsComparison.css';

function MetricsComparison({ clusters }) {
  const clusterList = Object.entries(clusters || {});

  if (clusterList.length === 0) {
    return <div className="metrics-empty">No clusters available</div>;
  }

  return (
    <div className="metrics-container">
      <table className="metrics-table">
        <thead>
          <tr>
            <th>Cluster</th>
            <th>Size</th>
            <th>%</th>
            <th>Avg Age</th>
            <th>Avg Income</th>
            <th>Avg Spending</th>
          </tr>
        </thead>
        <tbody>
          {clusterList.map(([clusterId, data]) => (
            <tr key={clusterId} className={`cluster-row cluster-${clusterId}`}>
              <td className="cluster-id-cell">{clusterId}</td>
              <td className="size-cell">{data.size}</td>
              <td className="percentage-cell">{data.percentage}%</td>
              <td className="metric-cell">
                {data.features['Age'] ? data.features['Age'].toFixed(2) : 'N/A'}
              </td>
              <td className="metric-cell">
                {data.features['Annual Income (k$)'] ? data.features['Annual Income (k$)'].toFixed(2) : 'N/A'}
              </td>
              <td className="metric-cell">
                {data.features['Spending Score (1-100)'] ? data.features['Spending Score (1-100)'].toFixed(2) : 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="cluster-distribution">
        <h4>Distribution:</h4>
        <div className="distribution-bars">
          {clusterList.map(([clusterId, data]) => (
            <div key={clusterId} className="bar-container">
              <div
                className={`bar cluster-${clusterId}`}
                style={{ height: `${Math.max(data.percentage * 2, 10)}px` }}
                title={`Cluster ${clusterId}: ${data.percentage}%`}
              />
              <span className="bar-label">C{clusterId}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default MetricsComparison;
