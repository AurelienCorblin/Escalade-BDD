import psycopg2
import psycopg2.extras

def connect():
  #rien besion de mettre car en localhost
  conn = psycopg2.connect(
    dbname = '',
    host = '',
    password = '',
    cursor_factory = psycopg2.extras.NamedTupleCursor
  )
  conn.autocommit = True
  return conn
