import os
import pandas as pd

def get_oracle_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'NUMBER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'NUMBER(1)'
    else:
        return 'VARCHAR2(255)'

def generate_table_creation_script(df, table_name):
    columns = []
    for col_name, dtype in zip(df.columns, df.dtypes):
        oracle_type = get_oracle_type(dtype)
        columns.append(f'"{col_name.upper()}" {oracle_type}')
    
    create_table_stmt = f'CREATE TABLE {table_name} (\n'
    create_table_stmt += ',\n'.join(columns)
    create_table_stmt += '\n);'

    return create_table_stmt

def process_excel_files(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            file_path = os.path.join(folder_path, file)
            excel = pd.ExcelFile(file_path)
            
            for sheet_name in excel.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write headers to .txt file
                txt_file_name = f'{file}-{sheet_name}.txt'
                with open(os.path.join(folder_path, txt_file_name), 'w') as txt_file:
                    txt_file.write('\n'.join(df.columns))
                
                # Generate Oracle table creation script and save it to .sql file
                table_name = f'{file}_{sheet_name}'.replace('-', '_').replace(' ', '_').replace('.', '_')
                create_table_stmt = generate_table_creation_script(df, table_name)
                sql_file_name = f'{file}-{sheet_name}.sql'
                with open(os.path.join(folder_path, sql_file_name), 'w') as sql_file:
                    sql_file.write(create_table_stmt)

if __name__ == '__main__':
    folder_path = 'path/to/your/excel/files'  # Update this with the path to your folder containing Excel files
    process_excel_files(folder_path)
