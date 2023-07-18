import pandas as pd
from pandas import DataFrame
import csv

def ID(array):
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in array:
            writer.writerow(row)
        file.close()
    result=ID_ALGM()
    return result

def ID_ALGM():
    df_yld = pd.read_csv("Project_file_train.csv")
    att_names = list(df_yld.columns)
    att_names.remove('YLD')

    def ent_of_list(lst):
        from collections import Counter
        cnt = Counter(x for x in lst)
        num = len(lst)*1
        probs = [x/num for x in cnt.values()]
        return ent(probs)

    def ent(probs):
        import math
        return sum([-prob*math.log(prob , 2) for prob in probs])

    def info_gain(df , split , target , trace=0):
        df_split = df.groupby(split)
        nobs = len(df.index)*1
        df_agg_ent = df_split.agg({target : [ent_of_list , lambda x : len(x)/nobs]})
        df_agg_ent.columns = ["entropy" , "propob"]
        new_ent = sum(df_agg_ent["entropy"]*df_agg_ent["propob"])
        old_ent = ent_of_list(df[target])
        print(split , " IG : " , old_ent-new_ent)
        return old_ent-new_ent

    def id3(df , target , attr_names , defclass = None):
        from collections import Counter
        cnt = Counter(x for x in df[target])
        if len(cnt)==1:
            return next(iter(cnt))
        elif df.empty or (not attr_names):
            return defclass
        else:
            defclass = max(cnt.keys())
            gain = [info_gain(df , attr , target) for attr in attr_names]
            index_max = gain.index(max(gain))
            bestat = attr_names[index_max]
            tree = {bestat:{}}
            rem = [i for i in attr_names if i!=bestat]

            for atval , subset in df.groupby(bestat):
                subtree = id3(subset , target , rem , defclass)
                tree[bestat][atval] = subtree
            return tree

    from pprint import pprint
    tree = id3(df_yld , 'YLD' , att_names)
    pprint(tree)

    def predict(tree, instance):
        if not isinstance(tree, dict):
            return tree
        else:
            root_node = next(iter(tree))
            feature_value = instance[root_node]
            if feature_value in tree[root_node]:
                return predict(tree[root_node][feature_value], instance)
            else:
                return None

    def evaluate(tree, test_data_m, label):
        for index, row in test_data_m.iterrows():
            result = predict(tree, test_data_m.iloc[index])
            print("Predicted value =",result) 
            return result    
    test = pd.read_csv("data.csv")
    final_result=evaluate(tree , test,'YLD')
    return final_result
   
    
