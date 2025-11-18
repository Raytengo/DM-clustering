import React from 'react';
import './ClusterInfo.css';

function ClusterInfo({ prediction, clusterName }) {
  if (!prediction) {
    return <div className="cluster-info">No prediction yet</div>;
  }

  const profile = prediction.cluster_profile;

  return (
    <div className="cluster-info">
      <div className="cluster-header">
        <h3 className="cluster-name">{clusterName}</h3>
        <div className="cluster-id">Cluster {prediction.predicted_cluster}</div>
      </div>

      <div className="cluster-stats">
        <div className="stat-item">
          <span className="stat-label">Cluster Size:</span>
          <span className="stat-value">{profile.size} customers</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Percentage:</span>
          <span className="stat-value">{profile.percentage}%</span>
        </div>
      </div>

      <div className="cluster-features">
        <h4>Cluster Characteristics:</h4>
        <table className="features-table">
          <tbody>
            {Object.entries(profile.features || {}).map(([feature, value]) => (
              <tr key={feature}>
                <td className="feature-name">{formatFeatureName(feature)}</td>
                <td className="feature-value">{typeof value === 'number' ? value.toFixed(2) : value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="interpretation">
        <h4>🔍 Interpretation:</h4>
        <p className="interpretation-text">
          {getInterpretation(clusterName)}
        </p>
      </div>
    </div>
  );
}

function formatFeatureName(name) {
  const names = {
    'Age': 'Average Age',
    'Annual Income (k$)': 'Average Income',
    'Spending Score (1-100)': 'Average Spending Score',
    'Genre_Male': 'Male Percentage'
  };
  return names[name] || name;
}

function getInterpretation(clusterName) {
  const interpretations = {
    'High-Value Customers': 'Premium customers with high income and high spending. Your best customers for premium products and services.',
    'Standard Customers': 'Regular customers with average income and spending. Good target for promotions and loyalty programs.',
    'Budget Spenders': 'Cost-conscious customers despite lower income. Ideal for value-oriented products and discounts.',
    'Affluent but Cautious': 'High earners who don\'t spend much. Great opportunity for engagement campaigns.',
    'Low-Engagement Customers': 'Minimal spending despite moderate income. Opportunity for re-engagement campaigns.'
  };
  return interpretations[clusterName] || 'See your cluster profile above for details.';
}

export default ClusterInfo;
