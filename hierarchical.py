import os
import pandas as pd
from sklearn.cluster import AgglomerativeClustering

def agglomerative_clustering(feature_vectors, k):
    clustering = AgglomerativeClustering(n_clusters=k).fit(feature_vectors)
    return clustering.labels_

if __name__ == '__main__':
    file_name = input('Enter the name of the file containing the feature vectors: ')
    k = int(input('Enter the number of clusters: '))
    df = pd.read_csv(file_name, index_col=0)
    feature_vectors = df.values
    labels = agglomerative_clustering(feature_vectors, k)
    data = {'Method_Name': df.index, 'labels': labels}
    df = pd.DataFrame(data)
    file_name = os.path.splitext(file_name)[0]
    df.to_csv(f'{file_name}_clustering_hierarchical.csv', index=False)
    print('hierarchical clustering complete. Check file_name_clustering.csv for the results.')