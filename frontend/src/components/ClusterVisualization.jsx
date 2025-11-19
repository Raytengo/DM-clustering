import React, { useEffect, useRef } from 'react';
import './ClusterVisualization.css';

function ClusterVisualization({ data, prediction, algorithmName }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (data && canvasRef.current) {
      drawVisualization();
    }
  }, [data, prediction]);

  const drawVisualization = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const padding = 60;

    // Clear canvas
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);

    if (!data.points || data.points.length === 0) {
      ctx.fillStyle = '#999';
      ctx.font = '14px Arial';
      ctx.fillText('No data to visualize', 50, 50);
      return;
    }

    // Calculate bounds
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;

    data.points.forEach(point => {
      minX = Math.min(minX, point.x);
      maxX = Math.max(maxX, point.x);
      minY = Math.min(minY, point.y);
      maxY = Math.max(maxY, point.y);
    });

    const rangeX = maxX - minX || 1;
    const rangeY = maxY - minY || 1;
    const scale = 0.9;

    // Helper function to convert data to canvas coordinates
    const toCanvasX = (x) => padding + ((x - minX) / rangeX) * (width - 2 * padding) * scale;
    const toCanvasY = (y) => height - padding - ((y - minY) / rangeY) * (height - 2 * padding) * scale;

    // Draw axes
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.stroke();

    // Draw axis labels
    ctx.fillStyle = '#666';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Principal Component 1', width / 2, height - 10);
    ctx.save();
    ctx.translate(10, height / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Principal Component 2', 0, 0);
    ctx.restore();

    // Color scheme for clusters
    const colors = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
      '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#AED6F1'
    ];

    // Draw points
    data.points.forEach((point, idx) => {
      const x = toCanvasX(point.x);
      const y = toCanvasY(point.y);
      const color = colors[point.cluster % colors.length];

      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI);
      ctx.fill();

      ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
      ctx.lineWidth = 1;
      ctx.stroke();
    });

    // Draw prediction point if exists
    if (prediction && prediction.predicted_cluster !== undefined) {
      const x = toCanvasX(Math.random() * (rangeX * 0.2));
      const y = toCanvasY(Math.random() * (rangeY * 0.2));

      // Draw star for prediction
      drawStar(ctx, x, y, 15, '#FFD700', '#FF4500');
    }

    // Draw legend
    const uniqueClusters = [...new Set(data.points.map(p => p.cluster))];
    let legendY = padding + 20;
    
    ctx.font = 'bold 12px Arial';
    ctx.fillStyle = '#333';
    ctx.fillText('Clusters:', width - 120, legendY);
    legendY += 20;

    uniqueClusters.forEach((cluster, idx) => {
      const color = colors[cluster % colors.length];
      ctx.fillStyle = color;
      ctx.fillRect(width - 120, legendY - 10, 12, 12);
      
      ctx.fillStyle = '#333';
      ctx.font = '11px Arial';
      ctx.fillText(`Cluster ${cluster}`, width - 100, legendY);
      legendY += 18;
    });

    // Draw explanation variance
    if (data.explained_variance) {
      ctx.fillStyle = '#666';
      ctx.font = '11px Arial';
      const varStr = `Explained Var: ${(data.explained_variance[0] * 100).toFixed(1)}% + ${(data.explained_variance[1] * 100).toFixed(1)}%`;
      ctx.fillText(varStr, padding, height - 35);
    }
  };

  const drawStar = (ctx, cx, cy, spikes, outerColor, innerColor) => {
    let rot = Math.PI / 2 * 3;
    let step = Math.PI / spikes;

    ctx.beginPath();
    ctx.moveTo(cx, cy - 12);
    
    for (let i = 0; i < spikes; i++) {
      ctx.lineTo(Math.cos(rot) * 12 + cx, Math.sin(rot) * 12 + cy);
      rot += step;
      ctx.lineTo(Math.cos(rot) * 6 + cx, Math.sin(rot) * 6 + cy);
      rot += step;
    }
    
    ctx.lineTo(cx, cy - 12);
    ctx.closePath();
    ctx.fillStyle = outerColor;
    ctx.fill();
    ctx.strokeStyle = innerColor;
    ctx.lineWidth = 2;
    ctx.stroke();
  };

  return (
    <div className="visualization-container">
      <canvas 
        ref={canvasRef} 
        width={500} 
        height={400}
        className="cluster-canvas"
      />
      <p className="algorithm-label">{algorithmName}</p>
      {prediction && (
        <p className="prediction-indicator">
          ⭐ Your position: <strong>Cluster {prediction.predicted_cluster}</strong>
        </p>
      )}
    </div>
  );
}

export default ClusterVisualization;
