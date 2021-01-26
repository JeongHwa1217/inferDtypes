# library
import pandas as pd
import os
import matplotlib.pyplot as plt

"""
date는 제외
"""


def infer_dtypes(df):
    col_name = df.columns
    origin_dt = df.dtypes
    inferred_dt = []
    col_unique = []
    col_notNull = []
    col_pct = []
    col_label = []

    for col in col_name:
        unique_value = df[col].unique()
        unique_cnt = len(unique_value)
        notNull_cnt = df[col].notnull().sum()
        col_notNull.append(notNull_cnt)
        unique_pct = unique_cnt / notNull_cnt
        col_pct.append(unique_pct)

        if (unique_cnt == 2):
            dataType = 'binary'

        elif (origin_dt[col] == 'int64'):
            if (unique_cnt < 5 or unique_pct < 0.005):
                dataType = 'category'
            else:
                dataType = 'numerical'

        elif (origin_dt[col] == 'float64'):
            if (unique_cnt < 5 or unique_pct < 0.005):
                dataType = 'category'
            else:
                dataType = 'numerical'

        elif (origin_dt[col] == 'object'):
            if (unique_cnt < 10 or unique_pct < 0.1):
                dataType = 'category'
            else:
                dataType = 'text'

        # DON'T KNOW
        else:
            dataType = 'text'


        # Input / Output / except
        if (unique_pct == 1 or notNull_cnt/df.shape[0] < 0.7):
            col_label.append('except')

        # if column name contains 'label'
        elif ('label' in col.lower()):
            col_label.append('output')

        else:
            col_label.append('input')

        col_unique.append(unique_cnt)
        inferred_dt.append(dataType)

    result = pd.DataFrame(data={'origin': origin_dt, 'rule base': inferred_dt,
                                'unique': col_unique, 'total': col_notNull, 'pct': col_pct,
                                'label': col_label})

    # def convertType(inferType):
    #   if(inferType == "integer")

    #print(result)
    return result

def draw_graph(df, result):
    row_names = result.index.values

    for row_name in row_names:
        row = result.loc[row_name]
        dtype = row['rule base']

        if (dtype is 'text'):
            print(row_name, ': ')
            print('unique = ', row['unique'])

        elif (dtype is 'numerical'):
            # print(row_name)
            plt.hist(df[row_name])
            plt.title(row_name)
            #plt.show()

        elif (dtype is 'binary'):
            plt.pie(df[row_name].value_counts(), explode=[0, 0.1], startangle=90, autopct='%1.1f%%')
            plt.title(row_name)
            #plt.show()

        elif (dtype is 'category'):
            print(row_name, ': ')
            value_pct = df[row_name].value_counts(normalize=True, sort=True, ascending=False).head(2)
            value_pct.loc['others'] = 1 - sum(value_pct)
            [print(value_pct.index[i],'\t',format(value_pct.iloc[i], ".2%")) for i in range(3)]


if __name__ == "__main__":
    path_dir = './data'
    file_list = os.listdir(path_dir)


    # read data
    for file in file_list:
        try :
            df = pd.read_csv(path_dir+'/'+file)
            print(file, '\t', df.shape)
            result = infer_dtypes(df)
            result.to_csv('./result.csv', mode='a')
            graphs = draw_graph(df, result)
        except PermissionError:
            pass

    # df = pd.read_csv(path_dir+'/'+file_list[3])
    # result = infer_dtypes(df)
    # print(result)
    # draw_graph(df, result)
