* 如果你分析後打算要去掉不相關的特徵(提高準確率什麼的)，可以在 data.py 修改。(data.py 35行那邊)  
* K_NUM 變數可以修改群集數量 k。(以我使用的特徵,5是比較好的,但如果改變特徵了,可能需要再找找)(clustering.py 17行那邊)  
* 如果你想要修改cluster plot的xy軸label，可以在 def plot_clusters_2d 中進行更改。(clustering.py 82行那邊)  
* 圖片的內容還有模型輸出的summary我就不解釋了(我相信你可以看懂的😄),主要是用來讓我簡單判斷模型能不能用而已，替換掉或修改都可  




# Mall Customers Clustering Analysis

This project performs data preprocessing and clustering analysis on the Mall Customers dataset using K-Means++ and Ward's Agglomerative Clustering.

## Files

- `data.py`: Data preprocessing script.
- `clustering.py`: Clustering analysis script that uses processed data from `data.py`.
- `pic/`: Folder containing output plots (created automatically).

## Usage

### 1. Data Preprocessing (`data.py`)
Run `data.py` directly to see the original dataset information and the processed data.

```bash
python data.py
```

**Output:**
- Original dataset schema and first 5 rows.
- Processed dataset schema and first 5 rows (after cleaning, encoding, and scaling).

### 2. Clustering Analysis (`clustering.py`)
Run `clustering.py` to perform clustering using K-Means++ and Ward's method. It automatically uses the processed data from `data.py`.

Modify `K_NUM` at the top of `clustering.py` to change the number of clusters (k).

```bash
python clustering.py
```

**Output:**
- Analysis results for both K-Means++ and Ward's method, including silhouette scores, Calinski-Harabasz scores, and cluster summaries.
- Plots saved in the `pic/` folder:
  - Elbow plot for K-Means.
  - Scatter plots for clusters.
  - Dendrogram for Ward's method.
  

### 3. Clustering Visualization, Optimization and Explanation
Using the `pipeline.ipynb` to perform visualization, optimization and explain the cluster main feature in one pipeline. Using the data preprocessed form `data.py` and the methos from `clustering.py`.

- Visualization: Apply PCA and t-SNE for dimensionality reduction (reducing data to 2D), then visualize the data in its original form and after clustering with K-means.
- Optimization: Adopt hyperparameter search to find the optimal hyperparameters for K-means and Ward's method.
- Explanation: Identify prominent attributes of data within each cluster to assign human-readable labels.

### 4. Comprehensive Clustering Comparison (`clustering_comparison.ipynb`)
Advanced analysis notebook comparing three clustering algorithms:

```bash
jupyter notebook clustering_comparison.ipynb
```

**Features:**
- Implements DBSCAN, Agglomerative, and Divisive Clustering
- Compares using internal metrics (Silhouette, Davies-Bouldin, Calinski-Harabasz)
- Stability analysis with different random seeds
- Detailed cluster interpretation and profiling
- Business recommendations for each cluster

### 5. Interactive Web Application

An interactive React web app for real-time cluster exploration and prediction.


#### Manual Start
**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

Open **http://localhost:3000**

#### Features
- 🎯 Choose from 3 clustering algorithms
- 📝 Input customer profile (age, income, spending score)
- 🔮 Get instant cluster prediction
- 📊 View cluster visualization and statistics
- 🎨 Beautiful, responsive interface
