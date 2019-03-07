import pandas as pd
import os


class Create_Script:

    def __init__(self, file, delimiter):
        self.file = file
        self.delimiter = delimiter

    def call_tables(self):
        filename, file_extension = os.path.splitext(self.file)
        filename = filename.split('/')[len(filename.split('/'))-1]
        if file_extension == '.csv':
            chunk_size = 10 ** 2
            for chunk in pd.read_csv(self.file, encoding='latin1', error_bad_lines=False, delimiter=self.delimiter, chunksize=chunk_size):
                self.create_table(filename.replace(" ", "_"), chunk)
                break
                #pd.read_csv(self.file, encoding='latin1', error_bad_lines=False, delimiter=',', chunksize=chunk_size))

        else:
            xl = pd.ExcelFile(self.file, encoding='latin1', error_bad_lines=False)
            for itm in xl.sheet_names:
                print(itm)
                df1 = xl.parse(itm)
                self.create_table(itm, df1)

    def create_table(self, tab_name, df1):
        tab_name = tab_name.replace(" ", "_").split('\\')[-1:][0]
        data_type = " character varying(500)"
        str_query = 'CREATE TABLE {}( "ID" SERIAL UNIQUE, '.format(tab_name)
        prefix = ""
        str_cols = ""
        for col in df1.axes[1]:
            str_query += prefix + '"'+ col.replace(" ", "_")+'" ' + data_type
            str_cols += prefix + '"'+ col.replace(" ", "_")+'" '
            prefix = ", "
        str_query += ");"

        str_query += r" COPY {}({}) FROM '{}' WITH DELIMITER '{}' CSV HEADER ENCODING 'LATIN1';".format(tab_name, str_cols,
                                                                                                        self.file, self.delimiter)
        print(str_query)
        #self.db.execute_query(str_query)
