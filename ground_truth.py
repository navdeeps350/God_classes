import pandas as pd

class utility:

    def __init__(self):
        self.ground_truth_dict = {}

    def ground_truth(self, keywords, df_method_names):
        df_method_names = [method_name.lower() for method_name in df_method_names]

        for method_name in df_method_names:
            for keyword in list(keywords['keywords'].values):
                # print(method_name, keyword, keyword in method_name)
                if method_name not in self.ground_truth_dict and keyword in method_name:
                    # print(method_name, keyword)
                    self.ground_truth_dict[method_name] = keyword
                    break
        df_method_names_new = [method_name for method_name in df_method_names if method_name not in self.ground_truth_dict]
        for method_name in df_method_names_new:
            self.ground_truth_dict[method_name] = 'others'

        new_values_dict = {}
        for i, value in enumerate(set(self.ground_truth_dict.values())):
            new_values_dict[value] = i
        # print(new_values_dict)

        for key, value in self.ground_truth_dict.items():
            self.ground_truth_dict[key] = new_values_dict[value]

        return self.ground_truth_dict


if __name__ == '__main__':
    keywords = pd.read_csv('keywords.txt', header=None, names=['keywords'])
    # print(keywords)
    file_path = input('Enter the path of the file containing the feature vectors: ')
    df_lables = pd.read_csv(file_path, index_col=0)
    df_method_names = list(df_lables.index)
    utility_class = utility()
    grnd_dict = utility_class.ground_truth(keywords, df_method_names)
    # print(grnd_dict)
    data = {'Method_Name': list(grnd_dict.keys()), 'labels': list(grnd_dict.values())}
    grnd_frame = pd.DataFrame(data)
    # print(list(grnd_dict.keys()), list(grnd_dict.values()))
    # grnd_frame = pd.DataFrame.from_dict(grnd_dict, orient='index', columns=['labels'])
    # print(grnd_frame)
    sep = '.'

    grnd_frame.to_csv(f'{file_path.split(sep, 1)[0]}_ground_truth.csv', index=False)
    print(f'Ground truth labels are saved in {file_path.split(sep, 1)[0]}_ground_truth.csv')