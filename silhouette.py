import os
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

class SilhouetteScore:

    def __init__(self, feature_vectors):
        self.feature_vectors = feature_vectors

    def k_means_score(self, k):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(self.feature_vectors)
        score = silhouette_score(self.feature_vectors, kmeans.labels_, metric='euclidean')
        return score

    def agglomerative_clustering_score(self, k):
        clustering = AgglomerativeClustering(n_clusters=k).fit(self.feature_vectors)
        score = silhouette_score(self.feature_vectors, clustering.labels_, metric='euclidean')
        return score



if __name__ == '__main__':
    file_name = input('Enter the name of the file containing the feature vectors: ')
    df = pd.read_csv(file_name, index_col=0)
    score = SilhouetteScore(df.values)
    k_scores = []
    hierarchical_scores = []
    k = []
    for i in range(2, 31):
        k_score = score.k_means_score(i)
        h_score = score.agglomerative_clustering_score(i)
        k_scores.append(k_score)
        hierarchical_scores.append(h_score)
        k.append(i)
    data = {'num_clusters': k, 'k_means_silhouette_score': k_scores, 'hierarchical_clustering_silhouette_score': hierarchical_scores}
    df_scores = pd.DataFrame(data)
    df_scores.to_csv(f'silhouette_scores_{file_name}', index=False)
    print(f'scores have been saved. Check the file silhouette_scores_{file_name} for the results.')
