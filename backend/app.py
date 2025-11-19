"""
Flask backend API for Clustering Visualization
Serves clustering models and predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, fcluster
import joblib

app = Flask(__name__)
CORS(app)

# ============================================================================
# LOAD PREPROCESSED DATA AND TRAIN MODELS
# ============================================================================

def preprocess_data():
    """Load and preprocess the Mall Customers dataset"""
    # Try multiple paths for the CSV file
    csv_paths = [
        'Mall_Customers.csv',
        '../Mall_Customers.csv',
        '../../Mall_Customers.csv',
        os.path.join(os.path.dirname(__file__), '../Mall_Customers.csv')
    ]
    
    csv_file = None
    for path in csv_paths:
        if os.path.exists(path):
            csv_file = path
            break
    
    if csv_file is None:
        raise FileNotFoundError(f"Mall_Customers.csv not found. Tried: {csv_paths}")
    
    df = pd.read_csv(csv_file)
    df = df.drop(columns=['CustomerID'])
    
    # OneHot encode gender
    from sklearn.preprocessing import OneHotEncoder
    ohe = OneHotEncoder(drop='first', sparse_output=False)
    genre_encoded = ohe.fit_transform(df[['Genre']])
    genre_df = pd.DataFrame(genre_encoded, columns=ohe.get_feature_names_out(['Genre']))
    df = pd.concat([df.drop(columns=['Genre']), genre_df], axis=1)
    
    # Standardize numerical features
    scaler = StandardScaler()
    numerical_cols = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    return df, scaler

def train_models(X):
    """Train all three clustering models"""
    models = {}
    
    # DBSCAN
    db = DBSCAN(eps=0.5, min_samples=5)
    models['dbscan'] = db.fit_predict(X)
    
    # Agglomerative
    agg = AgglomerativeClustering(n_clusters=5, linkage='ward')
    models['agglomerative'] = agg.fit_predict(X)
    
    # Divisive (using hierarchical complete linkage)
    Z = linkage(X, method='complete')
    models['divisive'] = fcluster(Z, 5, criterion='maxclust') - 1
    
    return models, agg, Z

# Initialize on startup
try:
    print("🔄 Loading data...")
    df_processed, scaler = preprocess_data()
    print(f"✅ Data loaded: {df_processed.shape}")
    
    X = df_processed.values
    print(f"✅ Features: {df_processed.columns.tolist()}")
    
    print("🔄 Training models...")
    models_labels, agg_model, Z_divisive = train_models(X)
    print(f"✅ Models trained successfully")
    
    # Store feature names and scalers for later use
    feature_names = df_processed.columns.tolist()
    n_features = len(feature_names)
    print(f"✅ Backend initialized with {n_features} features")
except Exception as e:
    print(f"❌ Initialization error: {str(e)}")
    import traceback
    traceback.print_exc()
    raise

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_input(data_dict):
    """Normalize user input using the training data scaler"""
    try:
        # Create array with same order as training features
        raw_values = []
        for feature in feature_names:
            if feature in data_dict:
                raw_values.append(float(data_dict[feature]))
            else:
                return None, f"Missing feature: {feature}"
        
        raw_array = np.array(raw_values).reshape(1, -1)
        
        # Normalize numerical features
        normalized = raw_array.copy()
        normalized[:, [0, 1, 2]] = scaler.transform(raw_array[:, [0, 1, 2]])
        
        return normalized, None
    except Exception as e:
        return None, str(e)

def get_cluster_profile(cluster_id, algorithm):
    """Get profile of a cluster"""
    df = df_processed.copy()
    
    if algorithm == 'dbscan':
        labels = models_labels['dbscan']
    elif algorithm == 'agglomerative':
        labels = models_labels['agglomerative']
    else:  # divisive
        labels = models_labels['divisive']
    
    df['cluster'] = labels
    cluster_data = df[df['cluster'] == cluster_id]
    
    if len(cluster_data) == 0:
        return None
    
    profile = {
        'size': len(cluster_data),
        'percentage': round(len(cluster_data) / len(df) * 100, 2),
        'features': {}
    }
    
    for feature in feature_names:
        profile['features'][feature] = round(float(cluster_data[feature].mean()), 4)
    
    return profile

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

@app.route('/api/features', methods=['GET'])
def get_features():
    """Get feature information"""
    return jsonify({
        'features': feature_names,
        'n_features': n_features,
        'n_samples': len(X),
        'algorithms': ['dbscan', 'agglomerative', 'divisive']
    })

@app.route('/api/data-summary', methods=['GET'])
def get_data_summary():
    """Get summary statistics of the training data"""
    summary = {}
    for feature in feature_names:
        col = df_processed[feature]
        summary[feature] = {
            'min': float(col.min()),
            'max': float(col.max()),
            'mean': float(col.mean()),
            'std': float(col.std())
        }
    return jsonify(summary)

@app.route('/api/clusters', methods=['GET'])
def get_clusters():
    """Get cluster information"""
    algorithm = request.args.get('algorithm', 'agglomerative')
    
    if algorithm == 'dbscan':
        labels = models_labels['dbscan']
    elif algorithm == 'agglomerative':
        labels = models_labels['agglomerative']
    else:  # divisive
        labels = models_labels['divisive']
    
    clusters = {}
    for cluster_id in sorted(np.unique(labels)):
        if cluster_id == -1:  # Skip noise for DBSCAN
            continue
        profile = get_cluster_profile(cluster_id, algorithm)
        if profile:
            clusters[str(cluster_id)] = profile
    
    return jsonify({
        'algorithm': algorithm,
        'clusters': clusters,
        'total_clusters': len(clusters)
    })

@app.route('/api/predict', methods=['POST'])
def predict_cluster():
    """Predict cluster for user input"""
    try:
        data = request.json
        algorithm = data.get('algorithm', 'agglomerative')
        
        # Extract features
        user_input = {
            'Age': data.get('Age'),
            'Annual Income (k$)': data.get('income'),
            'Spending Score (1-100)': data.get('spending'),
            'Genre_Male': data.get('gender')  # 1 for male, 0 for female
        }
        
        # Normalize input
        normalized, error = normalize_input(user_input)
        if error:
            return jsonify({'error': error}), 400
        
        # Predict based on algorithm
        if algorithm == 'dbscan':
            db = DBSCAN(eps=0.5, min_samples=5)
            db.fit(X)
            # Use simple distance-based prediction for DBSCAN
            from sklearn.neighbors import NearestNeighbors
            nbrs = NearestNeighbors(n_neighbors=1).fit(X)
            distances, indices = nbrs.kneighbors(normalized)
            cluster_id = int(models_labels['dbscan'][indices[0][0]])
            
        elif algorithm == 'agglomerative':
            # For Agglomerative, use nearest neighbor in training data
            from sklearn.neighbors import NearestNeighbors
            nbrs = NearestNeighbors(n_neighbors=1).fit(X)
            distances, indices = nbrs.kneighbors(normalized)
            cluster_id = int(models_labels['agglomerative'][indices[0][0]])
            
        else:  # divisive
            # For Divisive, use nearest neighbor in training data
            from sklearn.neighbors import NearestNeighbors
            nbrs = NearestNeighbors(n_neighbors=1).fit(X)
            distances, indices = nbrs.kneighbors(normalized)
            cluster_id = int(models_labels['divisive'][indices[0][0]])
        
        # Get cluster profile
        profile = get_cluster_profile(cluster_id, algorithm)
        
        return jsonify({
            'success': True,
            'algorithm': algorithm,
            'predicted_cluster': cluster_id,
            'cluster_profile': profile,
            'input': user_input
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualize', methods=['POST'])
def get_visualization_data():
    """Get data for 2D visualization"""
    try:
        data = request.json
        algorithm = data.get('algorithm', 'agglomerative')
        
        # Validate algorithm
        if algorithm not in ['dbscan', 'agglomerative', 'divisive']:
            return jsonify({'error': f'Invalid algorithm: {algorithm}'}), 400
        
        # Apply PCA for 2D visualization
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        
        if algorithm == 'dbscan':
            labels = models_labels['dbscan']
        elif algorithm == 'agglomerative':
            labels = models_labels['agglomerative']
        else:
            labels = models_labels['divisive']
        
        # Ensure labels and X_pca have same length
        if len(labels) != len(X_pca):
            return jsonify({'error': f'Mismatch: {len(labels)} labels vs {len(X_pca)} points'}), 500
        
        # Prepare data for frontend
        points = []
        for i, (x, y) in enumerate(X_pca):
            points.append({
                'x': float(x),
                'y': float(y),
                'cluster': int(labels[i])
            })
        
        return jsonify({
            'algorithm': algorithm,
            'points': points,
            'explained_variance': [float(v) for v in pca.explained_variance_ratio_],
            'n_points': len(points)
        })
    
    except Exception as e:
        import traceback
        print(f"Visualization error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Clustering API Server")
    print("="*60)
    print("📍 Backend URL: http://127.0.0.1:5001")
    print("📊 Dataset: Mall_Customers.csv")
    print("🔧 Algorithms: DBSCAN, Agglomerative, Divisive")
    print("="*60 + "\n")
    
    app.run(debug=False, port=5001, use_reloader=False)
