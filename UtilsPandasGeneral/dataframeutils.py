
#vraca subset sa istim kolonama nakon renameanja (ne uzima redove u obzir)
#def subset_common_columns(df_source, df_target):
def subset_2df_on_common_columns(df_source, df_target):
    common_cols = df_target.columns.intersection(df_source.columns)
    #https://stackoverflow.com/questions/38969267/python-pandas-selecting-columns-from-a-dataframe-via-a-list-of-column-names
    return df_source.filter(common_cols), df_target.filter(common_cols)


def subset_2df_rows_on_common_ux(df_source_subset_cmpr, df_target_subset_cmpr, common_column):
        common_rows_by_ux=set(df_target_subset_cmpr[common_column])&set(df_source_subset_cmpr[common_column])
        #print("common_rows_recordid su ", common_rows_recordid)
        df_source_subset_cmpr_commonrows = df_source_subset_cmpr.loc[df_source_subset_cmpr[common_column].isin(common_rows_by_ux)]
        df_target_subset_cmpr_commonrows = df_target_subset_cmpr.loc[df_target_subset_cmpr[common_column].isin(common_rows_by_ux)]

        return df_source_subset_cmpr_commonrows, df_target_subset_cmpr_commonrows

def clean_duplicates(df):
    #ignore first column (uuid)
    print("Cleaning duplicates...")
    df = df.drop_duplicates(subset=df.columns[1:], keep='last')
    return df


##############################

#ovo realno dodati u cleaning
def object_to_num(target_meta, df_data):

    floatcols = target_meta[['COLUMN_NAME','TARGET_DECIMAL_SCALE']][target_meta['TARGET_DATA_TYPE'].isin(['decimal', 'float'])]
    floatcols.set_index('COLUMN_NAME',inplace=True)
    floatcols = floatcols.to_dict()['TARGET_DECIMAL_SCALE']
    
    intcols = target_meta['COLUMN_NAME'][target_meta['TARGET_DATA_TYPE'].isin(['int', 'tinyint'])].tolist()

    if len(floatcols)>0:
        print("floatcols su ", floatcols)
        for col in floatcols:
            if col.lower() in df_data.columns:
                #print("col je ", col, "sa decimalama ", floatcols[col])
                #df_target[col] = df_target[col].astype(float)
                #df_target[col] = df_target[col].round(numcols[col])
                print(f"Col {col} casting to float...")
                df_data[col.lower()] = df_data[col.lower()].astype(float)
                #df_source_mapped[col] = df_source_mapped[col].map(f'{{:.{numcols[col]}f}}'.format)
            else:
                print("Object to float. There is no column ", col)
    if len(intcols)>0:
        for col in intcols:
            if col.lower() in df_data.columns:
                #print("col je ", col)
                df_data[col.lower()] = df_data[col.lower()].astype('Int64') #TODO - bolje roundati
            else:
                print("Object to num. There is no column ", col)

   
    return df_data

#TODO - make it more generalisable. passing meta should be
#specific to CLEANING, du has to have GENERALISABLE helper functions
def object_to_bit(target_meta, df_data):
    bitcols = target_meta[['COLUMN_NAME']][target_meta['TARGET_DATA_TYPE'].isin(['bit', 'bool'])]
    bitcols = set(bitcols['COLUMN_NAME'])
    if len(bitcols)>0:
        #print("bitcols su ", bitcols)
        for col in bitcols:
            if col.lower() in df_data.columns:
                df_data = df_data.replace({col.lower(): {1: True, 0: False,'1': True, '0': False,'Yes': True, 'No': False,0.0:False, 1.0: True,'YES':1, 'NO':0}})
                #if df_data[col].isin([0,1]).any():
                #    df_data = df_data.replace({col: {1: True, 0: False}})
                #elif df_data[col].isin(['0','1']).any():
                #    df_data = df_data.replace({col: {'1': True, '0': False}})
                #elif df_data[col].isin(['No','Yes']).any():
                #    df_data = df_data.replace({col: {'Yes': True, 'No': False}})
            else:
                print("Object to bit. There is no column ", col)
    return df_data

#realno cleaning, transformation, nisam jos prebacio
def object_to_string(target_meta, df_data):
    if 'nationalrecordid' in df_data.columns:
        df_data['nationalrecordid'] = df_data['nationalrecordid'].astype(str)

    strcols = target_meta[['COLUMN_NAME']][target_meta['TARGET_DATA_TYPE'].isin(['varchar', 'char','nvarchar'])]
    strcols = set(strcols['COLUMN_NAME'])
    if len(strcols)>0:
        #print("str cols su ", strcols)
        for col in strcols:
            if col in df_data.columns:
                df_data[col.lower()] = df_data[col.lower()].astype(str)

    return df_data

