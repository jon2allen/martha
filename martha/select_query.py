# Module Imports
import mariadb
import sys
import re
import functools
try:
   from martha.load_var import *
except:
   from load_var import *

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    ntxt = re.sub(clean, '', text )
    return ntxt.strip()

def run_query( rec_id ):
    try:
        conn = mariadb.connect(
            user=load_var('DB_USERNAME'),
            password=load_var('DB_PASSWORD'),
            host="127.0.0.1",
            port=3306,
            database="martha"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}", e)
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    my_sql_qry = "SELECT title, source, ingredients, Directions, http from recipe where rec_id = ?"

    # my_sql_qry = my_sql_qry + "\'" + str(13) + "\'"



    #for item in cur:
    #   print(item)


    try:
        cur.execute(my_sql_qry, (rec_id,))
    except mariadb.Error as e:
        print(f"Error: {e}")
        return None

    item = cur.next()

 #   print( "item: ", item)
    if item == None:
        return None
    ing = item[2].split('   ')

    ing = list(filter(None, ing ))
#    print(ing)

    directions = item[3].split('<br>')

    directions = map(remove_html_tags, directions)

    directions = filter(None,directions)

#    print(list(directions)) 

    result = [item[0], item[1], ing, list(directions), item[4] ]
    conn.close()
    return result

def run_query_table( search):
    try:
            conn = mariadb.connect(
                user=load_var('DB_USERNAME'),
                password=load_var('DB_PASSWORD'),
                host="127.0.0.1",
                port=3306,
                database="martha"
            )
    except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}", e)
            sys.exit(1)

        # Get Cursor
    cur = conn.cursor()

    my_sql_qry = "SELECT rec_id, title, http from recipe where title like ?"
    search = "%" + search + "%"
    try:
        cur.execute(my_sql_qry, (search,))
    except mariadb.Error as e:
        print(f"Error: {e}")
        return None

    if cur.rowcount == 0:
        print("no reesutls from query")

    #for item in cur:
    #    print(item)
    rtn_list = [x for x in cur]
    conn.close()
    return rtn_list
    # return cur




if __name__ == "__main__":
    res = run_query(13)
    print(res)


    res = run_query_table("Ham")

    print(res)
