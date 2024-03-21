import javalang
import os
import pandas as pd
from collections import Counter


class GodClassFinder:

    def __init__(self, path: str):
        self.path = path
        self.god_class_dictionary = {'class_name': [], 'path': [], 'method_num': []}

    def find_god_classes(self):
        for (dirpath, dirnames, filenames) in os.walk("./resources/xerces2-j-src"):
            for filename in filenames:
                if filename.endswith('.java'):
                    # print(dirpath, filename)
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        tree = javalang.parse.parse(file.read())
                        for path, node in tree.filter(javalang.tree.ClassDeclaration):
                            method_num = 0
                            # print(node.name)
                            self.god_class_dictionary['class_name'].append(node.name)
                            self.god_class_dictionary['path'].append(os.path.join(dirpath, filename))
                            for path, method in node.filter(javalang.tree.MethodDeclaration):
                                # print(node.name)
                                method_num += 1
                            self.god_class_dictionary['method_num'].append(method_num)
        return self.god_class_dictionary      


if __name__ == '__main__':
    god_class_finder = GodClassFinder('./resources/xerces2-j-src')
    god_class_dataframe = pd.DataFrame.from_dict(god_class_finder.find_god_classes())
    mean = god_class_dataframe['method_num'].mean()
    standard_dev = god_class_dataframe['method_num'].std()
    god_class_dataframe.loc[god_class_dataframe['method_num'] > mean + 6 * standard_dev, ['class_name', 'path', 'method_num']].to_csv('god_classes.csv', index=False)
    god_classes = pd.read_csv('god_classes.csv')
