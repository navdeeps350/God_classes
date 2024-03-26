import javalang
import os
import pandas as pd
from collections import Counter

class utility:

    def get_fields(self, java_class):
        fields = []
        for path, node in java_class.filter(javalang.tree.FieldDeclaration):
            for declarator in node.declarators:
                fields.append(declarator.name)
        return fields

    def get_methods(self, java_class):
        methods = []
        methods_name = []
        for path, node in java_class.filter(javalang.tree.MethodDeclaration):
            methods.append(node)
            methods_name.append(node.name)
        return methods, methods_name

    def get_fields_accessed_by_method(self, method):
        fields = []
        accessed_field_counter = {}
        for path, node in method.filter(javalang.tree.MemberReference):
            # if isinstance(node.member, javalang.tree.VariableDeclarator):
            if node.qualifier != '':
                fields.append(node.qualifier)
            else:
                fields.append(node.member)
        accessed_field_counter = dict(Counter(fields))
        return fields, accessed_field_counter

    def get_methods_accessed_by_method(self, method):
        methods = []
        accessed_method_counter = {}
        for path, node in method.filter(javalang.tree.MethodInvocation):
            methods.append(node.member)
        accessed_method_counter = dict(Counter(methods))
        return methods, accessed_method_counter


if __name__ == '__main__':
    utility_class = utility()
    god_classes = pd.read_csv('god_classes.csv')
    god_class_list = god_classes['path'].tolist()
    for cls in god_class_list:
        nes_dict = {}
        with open(cls, 'r') as file:
            tree = javalang.parse.parse(file.read())
            for path, class_name in tree.filter(javalang.tree.ClassDeclaration):
                if class_name.name == cls.split('/')[-1].split('.')[0]:
                    method_list, methods_name_list = utility_class.get_methods(class_name)
                    for method in method_list:
                        nes_dict[f'{method.name}'] = {}
                    field_list = utility_class.get_fields(class_name)
                    for method in method_list:
                        accesses_field, accesses_field_dict = utility_class.get_fields_accessed_by_method(method)
                        accesses_method, accesses_method_dict = utility_class.get_methods_accessed_by_method(method)
                        for a_m in accesses_method:
                            if a_m not in methods_name_list:
                                accesses_method_dict.pop(a_m, None)
                        nes_dict[f'{method.name}'].update(accesses_method_dict)
                        for a_f in accesses_field:
                            if a_f not in field_list:
                                accesses_field_dict.pop(a_f, None)
                        nes_dict[f'{method.name}'].update(accesses_field_dict)

        row_list = list(set(methods_name_list))
        column_list = list(set(methods_name_list)) + list(set(field_list))
        df = pd.DataFrame(columns=column_list, index=row_list)

        for method_name in df.index:
            for field_name in df.columns:
                if method_name in nes_dict and field_name in nes_dict[method_name]:
                    df.loc[method_name, field_name] = 1
                else:
                    df.loc[method_name, field_name] = 0
        df.to_csv(f'{cls.split("/")[-1].split(".")[0]}.csv')
        print(f'{cls.split("/")[-1].split(".")[0]}.csv has been created.')


