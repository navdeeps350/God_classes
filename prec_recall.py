import pandas as pd
from itertools import combinations

class precision_recall:

    def __init__(self, clustering_frame, ground_truth_frame):
        self.clustering_frame = clustering_frame
        self.ground_truth_frame = ground_truth_frame

    def cluster_keys_by_value(self, dictionary):
        clusters = {}
        for key, value in dictionary.items():
            if value not in clusters:
                clusters[value] = [key]
            else:
                clusters[value].append(key)
        return clusters


    def get_sets(self, data_frame):
        pair_set = set()
        for i, lst in enumerate(list(self.cluster_keys_by_value(data_frame.to_dict()['labels']).values())):
            for c in list(combinations(lst, 2)):
                pair_set.add(frozenset(c))
        return pair_set
    
    def calculate_precision_recall(self):
        pair_set_clustering =  self.get_sets(self.clustering_frame)
        pair_set_ground_truth = self.get_sets(self.ground_truth_frame)
        precision = len(pair_set_clustering.intersection(pair_set_ground_truth))/len(pair_set_clustering)
        recall = len(pair_set_clustering.intersection(pair_set_ground_truth))/len(pair_set_ground_truth)
        return precision, recall


if __name__ == '__main__':
    
    input_clustering_file = input('Enter the name of the file containing the clustering results: ')
    input_ground_truth_file = input('Enter the name of the file containing the ground truth labels: ')
    df_clustering = pd.read_csv(input_clustering_file, index_col=0)
    df_ground_truth = pd.read_csv(input_ground_truth_file, index_col=0)
    
    prec_rec = precision_recall(df_clustering, df_ground_truth)

    precision, recall = prec_rec.calculate_precision_recall()
    print(f'Precision: {precision}, Recall: {recall}')
    # f_score = 2 * (precision * recall) / (precision + recall)

    # print(f'Precision: {precision}, Recall: {recall}, F1 Score: {f_score}')

    
