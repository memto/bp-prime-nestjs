import sys, os
import csv
import psycopg2
from dotenv import dotenv_values

config = dotenv_values("../.env")

if len(sys.argv) != 3:
  print("Usage: python3 theScript <CSV_FILE> <TABLE_NAME>")
  sys.exit(0)

input_csv = os.path.abspath(sys.argv[1])
table_name = sys.argv[2]

def connect():
  """ Connect to the PostgreSQL database server """
  conn = None
  try:
    # read connection parameters
    params = {
      "host": config['POSTGRES_HOST'],
      "database": config['POSTGRES_DB'],
      "user": config['POSTGRES_USER'],
      "password": config['POSTGRES_PASSWORD'],
    }

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

    # close the communication with the PostgreSQL
    cur.close()

    return conn
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  # finally:
  #   if conn is not None:
  #     conn.close()
  #     print('Database connection closed.')

def import_table_from_csv(db_conn, csv_file, table):  
  cur = db_conn.cursor()
  cur.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (table,))
  if bool(cur.rowcount):
    with open(csv_file, 'r') as file:
      csvreader = csv.reader(file, delimiter='\t')
      for row in csvreader:
        cur = db_conn.cursor()
        print(row)
        try:
          text = row[1].replace("'", "''")
          translate_text = row[4].replace("'", "''")
          query = f"INSERT INTO {table} VALUES ({row[0]}, '{text}', '{row[2]}', {row[3]}, '{translate_text}')"
          cur.execute(query)
        except psycopg2.errors.UniqueViolation as err:
          cur.execute("ROLLBACK")
          pass
        # break #== TO_TEST
      db_conn.commit()
  else:
    print('table not existed. run "npm run schema:sync" first')

if __name__ == '__main__':
  db_conn = connect()
  import_table_from_csv(db_conn, input_csv, table_name)
  db_conn.close()