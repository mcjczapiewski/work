# import csv
# import pyodbc

# mdb = r"D:\_MACIEK_\python_proby\proba\mdb\ZAKRES.mdb"
# drv = "{ODBC Driver 17 for SQL Server}"
# pwd = "pw"
# server = "tcp:myserver.database.windows.net"

# con = pyodbc.connect(
#     r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
#     r"DBQ=D:\_MACIEK_\python_proby\proba\mdb\ZAKRES.mdb"
# )
# cur = con.cursor()

# SQL = "SELECT * FROM ZASIEG"
# rows = cur.execute(SQL).fetchall()
# cur.close()
# con.close()

# with open(r"D:\_MACIEK_\python_proby\proba\mdb\aa.csv", "wb") as fou:
#     csv_writer = csv.writer(fou)
#     csv_writer.writerows(rows)

from meza import io

records = io.read(r"D:\_MACIEK_\python_proby\proba\mdb\ZAKRES.mdb")
print(next(records))
