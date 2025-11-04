import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score

try:
    from scipy.cluster.hierarchy import dendrogram, linkage
    SCIPY_AVAILABLE = True
except Exception:
    SCIPY_AVAILABLE = False

# Global k number for clustering
K_NUM = 5

# Import processed dataframe from data.py (expects `df` to be defined there)
try:
    from data import preprocess_data
    df = preprocess_data()
except Exception as e:
    print('Failed to import and preprocess data from data.py:', e)
    sys.exit(1)

OUT_DIR = 'pic'
os.makedirs(OUT_DIR, exist_ok=True)

# Run KMeans++ clustering
def run_kmeans(features, ks=range(2, 7)):
    results = {}
    inertias = []
    for k in ks:
        km = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
        labels = km.fit_predict(features)
        sil = silhouette_score(features, labels)
        ch = calinski_harabasz_score(features, labels)
        results[k] = {'model': km, 'labels': labels, 'silhouette': sil, 'calinski_harabasz': ch, 'inertia': km.inertia_}
        inertias.append(km.inertia_)
        print(f"KMeans k={k}: silhouette={sil:.3f}, calinski_harabasz={ch:.1f}, inertia={km.inertia_:.1f}")

    # Plot inertia (elbow)
    plt.figure(figsize=(6, 4))
    plt.plot(list(ks), inertias, marker='o')
    plt.xticks(list(ks))
    plt.xlabel('k (number of clusters)')
    plt.ylabel('Inertia')
    plt.title('KMeans Elbow Plot')
    plt.grid(True)
    elbow_path = os.path.join(OUT_DIR, 'kmeans_elbow.png')
    plt.tight_layout()
    plt.savefig(elbow_path)
    return results

# Run Ward's Agglomerative Clustering
def run_ward(features, n_clusters=5):
    # Agglomerative clustering with Ward linkage
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    labels = ward.fit_predict(features)
    sil = silhouette_score(features, labels)
    ch = calinski_harabasz_score(features, labels)
    print(f"Ward Agglomerative n_clusters={n_clusters}: silhouette={sil:.3f}, calinski_harabasz={ch:.1f}")

    # Dendrogram (requires scipy library, make sure it's installed)
    if SCIPY_AVAILABLE:
        Z = linkage(features, method='ward')
        plt.figure(figsize=(10, 4))
        dendrogram(Z, truncate_mode='level', p=5)
        plt.title('Ward Dendrogram (truncated)')
        dend_path = os.path.join(OUT_DIR, 'ward_dendrogram.png')
        plt.tight_layout()
        plt.savefig(dend_path)
    else:
        print('scipy not available — skipping dendrogram (install scipy to enable)')

    return {'model': ward, 'labels': labels, 'silhouette': sil, 'calinski_harabasz': ch}

# Visualization of clusters in 2D (using first two features for default, can be modified)
def plot_clusters_2d(features, labels, title_prefix='cluster', save_name='clusters.png'):
    cols = list(features.columns) if hasattr(features, 'columns') else []
    if 'Annual Income (k$)' in cols and 'Spending Score (1-100)' in cols: # Modified xcol, ycol label here
        xcol, ycol = 'Annual Income (k$)', 'Spending Score (1-100)'
    else:
        # fallback to first two columns
        xcol, ycol = cols[0], cols[1]

    plt.figure(figsize=(6, 5))
    sns.scatterplot(x=features[xcol], y=features[ycol], hue=labels, palette='tab10', legend='full')
    plt.title(f'{title_prefix}: {xcol} vs {ycol}')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, save_name)
    plt.savefig(path)

def summarize_clusters(features, labels):
    dfc = features.copy()
    dfc['Cluster'] = labels
    summary = dfc.groupby('Cluster').agg(['mean','count'])
    print('\nCluster summary (mean and count):')
    print(summary)

def main():
    # features: use all columns in df (already preprocessed in data.py)
    features = df.copy()

    # Run KMeans with range up to K_NUM for elbow plot, but use K_NUM as final k
    print(f'\nRunning KMeans++ (testing k from 2 to {K_NUM} for elbow plot)')
    kmeans_results = run_kmeans(features, ks=range(2, K_NUM+1))

    labels = kmeans_results[K_NUM]['labels']
    plot_clusters_2d(df, labels, title_prefix=f'KMeans (k={K_NUM})', save_name=f'kmeans_k{K_NUM}_clusters.png')
    summarize_clusters(df, labels)

    print("\n----------------------------------------------")
    # Run Ward's method with same k
    print(f'\nRunning Ward\'s method (Agglomerative Clustering, n_clusters={K_NUM})')
    ward_res = run_ward(features, n_clusters=K_NUM)
    plot_clusters_2d(df, ward_res['labels'], title_prefix=f'Ward (n={K_NUM})', save_name=f'ward_n{K_NUM}_clusters.png')
    summarize_clusters(df, ward_res['labels'])

if __name__ == '__main__':
    main()
