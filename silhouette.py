import os
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering


def k_means_score(feature_vectors, k):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(feature_vectors)
    score = silhouette_score(df.values, kmeans.labels_, metric='euclidean')
    return score

def agglomerative_clustering_score(feature_vectors, k):
    clustering = AgglomerativeClustering(n_clusters=k).fit(feature_vectors)
    score = silhouette_score(df.values, clustering.labels_, metric='euclidean')
    return score



if __name__ == '__main__':
    file_name = input('Enter the name of the file containing the feature vectors: ')
    df = pd.read_csv(file_name, index_col=0)
    k_scores = []
    hierarchical_scores = []
    k = []
    for i in range(2, 31):
        k_score = k_means_score(df.values, i)
        h_score = agglomerative_clustering_score(df.values, i)
        k_scores.append(k_score)
        hierarchical_scores.append(h_score)
        k.append(i)
    data = {'num_clusters': k, 'k_means_silhouette_score': k_scores, 'hierarchical_clustering_silhouette_score': hierarchical_scores}
    df_scores = pd.DataFrame(data)
    print(df_scores)
