# library
import pandas as pd
import os

"""
date는 제외

"""



def predict_dtypes(df):
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
        #if (unique_pct==1 and dataType =='text'):
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

    print(result)
    return result


if __name__ == "__main__":
    path_dir = './data'
    file_list = os.listdir(path_dir)

    # read data
    for file in file_list:
        df = pd.read_csv(path_dir+'/'+file)
        print(file, '\t', df.shape)
        predict_dtypes(df)
        print('\n')
