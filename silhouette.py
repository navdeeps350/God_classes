import os
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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
    feature_file_path = input('Enter the path of the file containing the feature vectors: ')
    clustering_file_path = input('Enter the path of the file containing the clustering results: ')
    df_feature = pd.read_csv(feature_file_path, index_col=0)
    # print(df_feature.shape)
    pca = PCA(2)
    df_feature_2d = pca.fit_transform(df_feature)
    # print(df_feature_2d.shape)

    try:
        df_cluster = pd.read_csv(clustering_file_path, index_col=0)
        score = silhouette_score(df_feature.values, df_cluster['labels'].values, metric='euclidean')
        print(f'The silhouette score is {score}')
    except:
        score = SilhouetteScore(df_feature.values)
        k_scores = []
        hierarchical_scores = []
        k = []
        for i in range(2, 60):
            k_score = score.k_means_score(i)
            h_score = score.agglomerative_clustering_score(i)
            k_scores.append(k_score)
            hierarchical_scores.append(h_score)
            k.append(i)
        data = {'num_clusters': k, 'k_means_silhouette_score': k_scores, 'hierarchical_clustering_silhouette_score': hierarchical_scores}
        df_scores = pd.DataFrame(data)
        # print(df_scores['k_means_silhouette_score'].max())
        result_k_mean = list(df_scores.loc[df_scores['k_means_silhouette_score'] == df_scores['k_means_silhouette_score'].max(), 'num_clusters'])[0]
        result_hierarchical = list(df_scores.loc[df_scores['hierarchical_clustering_silhouette_score'] == df_scores['hierarchical_clustering_silhouette_score'].max(), 'num_clusters'])[0]
        print(f'The optimal number of clusters for k-means is {result_k_mean}')
        print(f'The optimal number of clusters for hierarchical clustering is {result_hierarchical}')
        plt.plot(k, k_scores, label='k-means')
        plt.plot(k, hierarchical_scores, label='hierarchical clustering')
        plt.xlabel('Number of clusters')
        plt.ylabel('Silhouette score')
        plt.legend()

        sep = '.'
        plt.savefig(f'{feature_file_path.split(sep, 1)[0]}_silhouette_scores.png')
        plt.show()
        
        df_scores.to_csv(f'{feature_file_path.split(sep, 1)[0]}_silhouette_scores.csv', index=False)
        print(f'scores have been saved. Check the file silhouette_scores_{feature_file_path} for the results.')
