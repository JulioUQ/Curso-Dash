import pyodbc 
import pandas as pd

def consulta(querystring):
    cnxn = pyodbc.connect(
                "Driver= {SQL Server};"
                "Server=server;"
                "Database=database;"
                "Trusted_Connection=no;"
                "UID=user;"
                "PWD=password"
                )
    result= pd.read_sql_query(querystring, con=cnxn)

    cnxn.close()

    return result