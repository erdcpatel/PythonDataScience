'''
To load the Excel file data to an Oracle table, you can use the pandas, cx_Oracle, and os libraries.
Make sure to have them installed before running the script. The script below reads the Excel, CSV,
and TXT files in a given folder, validates the headers based on the configuration,
and loads the data into the corresponding Oracle tables. It also adds an audit column PROCESS_ID to the data.
'''

import os
import pandas as pd
import cx_Oracle

def read_data(file_path):
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.txt'):
        return pd.read_csv(file_path, sep='\t')  # Assuming tab-separated data in .txt files
    else:
        raise ValueError(f'Unsupported file format: {file_path}')

def load_data_to_oracle(file_path, table_name, connection, process_id, header_config):
    df = read_data(file_path)

    # Validate the header
    header = '|'.join(df.columns)
    if header != header_config[table_name]:
        raise ValueError(f'Header validation failed for {file_path}. Expected: {header_config[table_name]}, found: {header}')

    # Add the audit column for the unique process ID
    df['PROCESS_ID'] = process_id

    # Load the data to the Oracle table
    df.to_sql(table_name, con=connection, if_exists='append', index=False)

def process_files(folder_path, connection, header_config, process_id):
    for file in os.listdir(folder_path):
        if file.endswith(('.xlsx', '.xls', '.csv', '.txt')):
            file_path = os.path.join(folder_path, file)
            table_name = ...  # Determine the table name from the configuration based on the file name
            load_data_to_oracle(file_path, table_name, connection, process_id, header_config)

if __name__ == '__main__':
    folder_path = 'path/to/your/files'  # Update this with the path to your folder containing Excel, CSV, and TXT files
    header_config = {
        'TABLE1': 'column1|column2|column3',
        'TABLE2': 'column1|column2|column3|column4',
        # Add more table and header configurations
    }

    # Oracle connection
    connection = cx_Oracle.connect('username', 'password', 'hostname:port/service_name')

    # Unique process ID
    process_id = 1  # Replace this with a unique process ID generator

    process_files(folder_path, connection, header_config, process_id)


''''''''''''''''''''''''''

transformation_config = {
    'file1.xlsx': {
        'date_column': ('to_datetime', '%Y-%m-%d'),
        'text_column': ('strip',),
    },
    'file2.csv': {
        'date_column': ('to_datetime', '%d/%m/%Y'),
    },
    # Add more file and transformation configurations
}


import os
import pandas as pd
import cx_Oracle

def read_data(file_path):
    # ... (same as before)

def apply_transformations(df, transformations):
    for column, (transformation, *args) in transformations.items():
        if transformation == 'to_datetime':
            df[column] = pd.to_datetime(df[column], format=args[0])
        elif transformation == 'strip':
            df[column] = df[column].str.strip()

def load_data_to_oracle(file_path, table_name, connection, process_id, header_config, transformation_config):
    df = read_data(file_path)

    # Validate the header
    # ... (same as before)

    # Apply transformations if configured
    if file_path in transformation_config:
        apply_transformations(df, transformation_config[file_path])

    # Add the audit column for the unique process ID
    # ... (same as before)

    # Load the data to the Oracle table
    # ... (same as before)

def process_files(folder_path, connection, header_config, process_id, transformation_config):
    # ... (same as before)

if __name__ == '__main__':
    folder_path = 'path/to/your/files'  # Update this with the path to your folder containing Excel, CSV, and TXT files
    header_config = {
        # ... (same as before)
    }
    transformation_config = {
        # ... (use the example format shown earlier)
    }

    # Oracle connection
    # ... (same as before)

    # Unique process ID
    # ... (same as before)

    process_files(folder_path, connection, header_config, process_id, transformation_config)


'''''''''''''
transformation_config = {
    'file1.xlsx': {
        'date_column': ('to_datetime', '%Y-%m-%d'),
        'text_column': ('strip',),
        'column1': ('fillna', 'N/A'),
        'column2': ('replace_value', 'old_value', 'new_value'),
        'column3': ('upper',),
        'column4': ('multiply', 2),
        'column5': ('add', 5),
    },
    # Add more file and transformation configurations
}


def apply_transformations(df, transformations):
    for column, (transformation, *args) in transformations.items():
        if transformation == 'to_datetime':
            df[column] = pd.to_datetime(df[column], format=args[0])
        elif transformation == 'strip':
            df[column] = df[column].str.strip()
        elif transformation == 'fillna':
            df[column] = df[column].fillna(args[0])
        elif transformation == 'replace_value':
            df[column] = df[column].replace(args[0], args[1])
        elif transformation == 'upper':
            df[column] = df[column].str.upper()
        elif transformation == 'lower':
            df[column] = df[column].str.lower()
        elif transformation == 'lstrip':
            df[column] = df[column].str.lstrip()
        elif transformation == 'rstrip':
            df[column] = df[column].str.rstrip()
        elif transformation == 'multiply':
            df[column] = df[column] * args[0]
        elif transformation == 'divide':
            df[column] = df[column] / args[0]
        elif transformation == 'add':
            df[column] = df[column] + args[0]
        elif transformation == 'subtract':
            df[column] = df[column] - args[0]


''''''''''''''''''''''''''
def get_oracle_table_data_types(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name, data_type FROM all_tab_columns WHERE table_name = '{table_name.upper()}'")

    data_types = {}
    for row in cursor.fetchall():
        column_name, data_type = row
        data_types[column_name] = data_type

    return data_types


def validate_data_types(df, oracle_data_types):
    for column, data_type in oracle_data_types.items():
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")

        if data_type == 'NUMBER' and not (pd.api.types.is_integer_dtype(df[column]) or pd.api.types.is_float_dtype(df[column])):
            raise ValueError(f"Invalid data type for column '{column}': Expected NUMBER")
        elif data_type == 'VARCHAR2' and not pd.api.types.is_string_dtype(df[column]):
            raise ValueError(f"Invalid data type for column '{column}': Expected VARCHAR2")
        elif data_type == 'DATE' and not pd.api.types.is_datetime64_dtype(df[column]):
            raise ValueError(f"Invalid data type for column '{column}': Expected DATE")
        # Add more data type checks if needed


def load_data_to_oracle(file_path, table_name, connection, process_id, header_config, transformation_config):
    df = read_data(file_path)

    # Validate the header
    # ... (same as before)

    # Apply transformations if configured
    if file_path in transformation_config:
        apply_transformations(df, transformation_config[file_path])

    # Validate data types against Oracle table
    oracle_data_types = get_oracle_table_data_types(connection, table_name)
    validate_data_types(df, oracle_data_types)

    # Add the audit column for the unique process ID
    # ... (same as before)

    # Load the data to the Oracle table
    # ... (same as before)


''''''''''''''''''''''''''''''
'''
There are several additional features that can be added to enhance the functionality and robustness of this script. Some of these features include:

Error handling and logging: Implement better error handling and logging to track any issues that occur during the process. This can help diagnose problems and improve maintainability.

Configuration file: Instead of hardcoding configurations (like header and transformation configurations) in the script, store them in a separate JSON, YAML, or INI file. This will make it easier to manage and update the configurations without modifying the script.

Parallel processing: If you have a large number of files to process, consider parallelizing the file processing using Python's concurrent.futures or multiprocessing libraries. This can significantly speed up the process by utilizing multiple CPU cores.

Incremental data loading: Implement incremental data loading to only load new or updated records into the Oracle database. This can be done by tracking the last processed timestamp or using a unique key to identify updated records.

Data validation: In addition to data type validation, you can implement more advanced data validation rules, such as checking for data inconsistencies or business rule violations.

Monitoring and notifications: Implement monitoring and notifications to track the progress of the data loading process and alert you in case of any issues.

Command-line interface: Create a command-line interface for the script to make it more user-friendly and easier to integrate into automated workflows or scheduling systems.

Retries and error recovery: Implement a retry mechanism for loading data into the Oracle database in case of temporary issues like network failures or timeouts. This can help make the script more resilient and less prone to failure.

Support for additional file formats: Add support for more file formats, such as Parquet, Avro, or JSON, based on your specific requirements.

Data transformation pipeline: Implement a more flexible and modular data transformation pipeline to easily chain multiple transformations and apply them in a specific order. This can be done using a library like Apache Beam or custom Python classes and functions.

These are just a few ideas to enhance the script and make it more robust, scalable, and flexible for various use cases. Depending on your specific requirements and the complexity of the data and transformations, you can choose to implement one or more of these additional features.
'''

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


'''Parallel Processing'''
from concurrent.futures import ThreadPoolExecutor

def process_files(folder_path, connection, process_id, config):
    # ... (same as before)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(load_data_to_oracle, file_path, table_name, connection, process_id, config) for file_path, table_name in files_to_process]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error processing file: {e}")


'''Custom Validation'''
def validate_positive_numbers(df, column):
    if any(df[column] < 0):
        raise ValueError(f"Invalid value in column '{column}': All values should be positive")

def validate_data(df, validation_config):
    for column, validation in validation_config.items():
        if validation == 'positive_numbers':
            validate_positive_numbers(df, column)
        # Add more validation functions as needed


'''Retry for oracle insert'''
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
def load_data_to_oracle_with_retry(file_path, table_name, connection, process_id, config):
    load_data_to_oracle(file_path, table_name, connection, process_id, config)

# In the process_files function, replace the call to load_data_to_oracle with load_data_to_oracle_with_retry

'''config.ini'''

[general]
process_id = 1234
folder_path = /path/to/your/files

[header_config]
file1.xlsx = header1,header2,header3
file2.xlsx = header1,header2,header3,header4

[transformation_config]
file1.xlsx.column1 = to_datetime, %Y-%m-%d
file1.xlsx.column2 = strip
file1.xlsx.column3 = fillna, N/A

[validation_config]
file1.xlsx.column1 = positive_numbers

[oracle_config]
username = your_username
password = your_password
dsn = your_dsn


import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Access a specific configuration value
process_id = config.getint('general', 'process_id')

'''Transformation'''
'''id	file_name	column_name	transformation_type	parameters	created_at	updated_at	user_id'''

#Params - {"format": "%Y-%m-%d"}

import json

def load_transformation_config(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT file_name, column_name, transformation_type, parameters FROM transformation_config")

    transformation_config = {}
    for row in cursor.fetchall():
        file_name, column_name, transformation_type, parameters = row
        if file_name not in transformation_config:
            transformation_config[file_name] = {}
        transformation_config[file_name][column_name] = (transformation_type, json.loads(parameters))

    return transformation_config

'''
Support custom transformations: To support custom transformations, you can define custom transformation functions 
in the script and register them in a dictionary. When applying transformations, look up the transformation 
function in the dictionary and call it with the provided parameters.

Here's an example of defining a custom transformation function and applying transformations using a dictionary:
'''
def custom_transformation(value, param1, param2):
    # Implement your custom transformation logic here
    return transformed_value

transformation_functions = {
    "to_datetime": to_datetime,
    "strip": strip,
    "fillna": fillna,
    "custom_transformation": custom_transformation
}

def apply_transformation(df, column, transformation, parameters):
    transformation_function = transformation_functions[transformation]
    df[column] = df[column].apply(transformation_function, **parameters)
