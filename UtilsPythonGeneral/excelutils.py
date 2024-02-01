import pandas as pd
from datetime import datetime
from pathlib import Path, PurePath

#TODO - bad init, try to make it more generalisable to use for non META test!
class ExcelCustom():
    def __init__(self):
        #self.df = dataframe_to_write
        self.file_full_path = None
        self.writer = None
        self.workbook = None

    def _createfolder_getpath_mainchecks_absolutepath(self,MAIN_FOLDER_PATH,DQ_SHEET_NAME):
        RESULTS_SUBFOLDER_LVL1_LOOKUP_NAME = DQ_SHEET_NAME #za RESULTS/dlookup name
        RESULTS_SUBFOLDER_LVL1_LOOKUP_DATE = datetime.today().strftime('%Y-%m-%d') #za RESULTS/dlookup name/current date
        RESULT_PATH = PurePath(MAIN_FOLDER_PATH,'RESULTS',RESULTS_SUBFOLDER_LVL1_LOOKUP_NAME,RESULTS_SUBFOLDER_LVL1_LOOKUP_DATE)
        Path(RESULT_PATH).mkdir(parents=True, exist_ok=True)
        return RESULT_PATH


    def determine_file_name_mainchecks(self,META,MAIN_FOLDER_PATH,DQ_SHEET_NAME):
        #TODO - improve - update on update, now is only once
        filename_template =f"QC-{META['TARGET_DB']}.{META['TARGET_SCHEMA']}.{META['TARGET_TABLE']}-vs-{META['SOURCE_DB']}.{META['SOURCE_SCHEMA']}.{META['SOURCE_TABLE']}"
        full_path_folder = self._createfolder_getpath_mainchecks_absolutepath(MAIN_FOLDER_PATH,DQ_SHEET_NAME)
        version=1

        def _generate_full_path(ver):  
            full_filename = f"{filename_template}_{datetime.today().strftime('%Y-%m-%d')}_v{str(ver)}.xlsx"
            #my_file = Path(full_path_folder)/Path(full_filename)
            return Path(full_path_folder)/Path(full_filename)
        my_file = _generate_full_path(version)

        while my_file.is_file() == True:
            print(f"Output version {str(version)} was already done today, creating next version...")
            version+=1
            my_file=_generate_full_path(version)
        else:
            self.file_full_path = my_file


        self.writer = pd.ExcelWriter(self.file_full_path, engine="xlsxwriter") # prev without engine="xlsxwriter"
        self.workbook =self.writer.book

    def determine_file_name_regular(self,MAIN_FOLDER_PATH,FILENAME):
        Path(MAIN_FOLDER_PATH).mkdir(parents=True, exist_ok=True)
        filename =FILENAME
        full_filename = f"{filename}_{datetime.today().strftime('%Y-%m-%d')}.xlsx"
        my_file = Path(MAIN_FOLDER_PATH)/Path(full_filename)
        if my_file.is_file():
            print("Check was already done today, creating a new version...")
            self.file_full_path = f"{my_file}-UPDATE.xlsx"
        else:
            self.file_full_path = my_file
        self.writer = pd.ExcelWriter(self.file_full_path, engine="xlsxwriter") # prev without engine="xlsxwriter"
        self.workbook =self.writer.book


    def _helper_extend_columns1(self,df, sheetname):
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            self.writer.sheets[sheetname].set_column(col_idx, col_idx, column_width)

    def _helper_extend_columns2(self,df, sheetname='Results'):
        worksheet = self.writer.sheets[sheetname]
        # Get the dimensions of the dataframe.
        (max_row, max_col) = df.shape
        # Make the columns wider for clarity.
        worksheet.set_column(0, max_col - 1, 12)
        # Set the autofilter.
        worksheet.autofilter(0, 0, max_row, max_col - 1)
   
    def write_df_regular(self,df, sheetname='Results'):
        #self.df.to_excel(self.writer, sheet_name='Results', index=False, na_rep='NaN')
        df.to_excel(self.writer, sheet_name=sheetname, index=False)

        self._helper_extend_columns2(df, sheetname)

    def write_df_multiindexlvl2(self,df,sheetname='Results'):
        df1 = pd.DataFrame(columns=df.droplevel([1], axis=1).columns)
        df2 = df.droplevel(0, axis=1)

        df1.to_excel(self.writer, sheet_name=sheetname)
        df2.to_excel(self.writer, sheet_name=sheetname, merge_cells = True, startrow=1)
        self._helper_extend_columns2(df2, sheetname)


    def save_excel(self):
        #TODO - add logic
        self.writer.close()

