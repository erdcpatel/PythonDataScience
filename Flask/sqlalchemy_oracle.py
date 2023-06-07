from sqlalchemy import create_engine

# Create an Oracle connection using SQLAlchemy
# Replace the connection string with your own Oracle database details
# Format: 'oracle+cx_oracle://<username>:<password>@<hostname>:<port>/<sid>'
connection_string = 'oracle+cx_oracle://username:password@hostname:port/sid'
engine = create_engine(connection_string)

# Establish a connection
with engine.connect() as connection:
    # Execute a SELECT query
    query = 'SELECT * FROM your_table_name'
    result = connection.execute(query)

    # Print the query result
    for row in result:
        print(row)

# Close the connection
engine.dispose()
