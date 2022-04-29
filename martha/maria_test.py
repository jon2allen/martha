# Module Imports
import mariadb
import sys
import re
import functools
from load_var import *

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    ntxt = re.sub(clean, '', text )
    return ntxt.strip()

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=load_var('DB_USERNAME'),
        password=load_var('DB_PASSWORD'),
        host="127.0.0.1",
        port=3306,
        database="martha"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

try:
    cur.execute(" select rec_id, title from recipe where rec_id < 25;")
except mariadb.Error as e:
    print(f"Error: {e}")

my_sql_qry = "SELECT title, source, ingredients, Directions, http from recipe where rec_id = ?"

# my_sql_qry = my_sql_qry + "\'" + str(13) + "\'"

print(my_sql_qry)

print(cur)

for item in cur:
   print(item)


try:
    cur.execute(my_sql_qry, (14,))
except mariadb.Error as e:
    print(f"Error: {e}")

for item in cur:
   print(item)

ing = item[2].split('   ')

ing = list(filter(None, ing ))
print(ing)

directions = item[3].split('<br>')

directions = map(remove_html_tags, directions)

directions = filter(None,directions)

print(list(directions)) 
