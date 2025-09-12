import pyodbc 
import pandas as pd

def consulta(querystring):
    cnxn = pyodbc.connect(
                "Driver= {SQL Server};"
                "Server=172.19.10.226,1533;"
                "Database=SGP_SIPE;"
                "Trusted_Connection=no;"
                "UID=user_cuadrosM;"
                "PWD=w$gh84Con2"
                )
    result= pd.read_sql_query(querystring, con=cnxn)

    cnxn.close()

    return result