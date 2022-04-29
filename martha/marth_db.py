# Module Imports
import mariadb
import sys
import re
import functools
try:
   from martha.load_var import *
except:
   from load_var import *

class martha_db():
    database = "martha"
    port = 3306
    host = "127.0.0.1"
    def __init__( self, user, password):
        self.user = user
        self.password = password  
    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        ntxt = re.sub(clean, '', text )
        return ntxt.strip()

    def run_query( self, rec_id ):
        print("run_query_rec_id")
        conn = self.init_db()
        # Get Cursor
        cur = conn.cursor(buffered=True)

        my_sql_qry = "SELECT title, source, ingredients, Directions, http, created, category from recipe where rec_id = ?"

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

        directions = map(self.remove_html_tags, directions)

        directions = filter(None,directions)

    #    print(list(directions)) 
    #    print("item:" , item )
        result = [item[0], item[1], ing, list(directions), item[4], item[5], item[6]]
        conn.close()
        return result

    def update_rec( self, rec_id, field, value ):
        conn = self.init_db()
        # Get Cursor
        cur = conn.cursor(buffered=True)
        

        my_sql_qry = "UPDATE recipe set " + field + "='" +  value + "'" 

        my_sql_qry = my_sql_qry + " where rec_id = " + str(rec_id)

        print("my_sql_qry:", my_sql_qry)

        try:
            cur.execute(my_sql_qry)
        except mariadb.Error as e:
            print(f"Error: {e}")
            return None
 
        conn.close()

        if cur.rowcount == 1:
            return True
        else:
            return False
    

    def run_query_get_all( self, limit = 0):
        conn = self.init_db()

            # Get Cursor
        cur = conn.cursor(buffered=True)
        ing = " Where Ingredients > \"\""
        if limit == 0:
            my_sql_qry = "SELECT rec_id, title, http from recipe" + ing
        else:
            my_sql_qry = "SELECT rec_id, title, http from recipe" + ing + " LIMIT " + str(limit)

        
        try:
            cur.execute(my_sql_qry)
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
    def run_query_table( self, search):
        conn = self.init_db()

            # Get Cursor
        cur = conn.cursor(buffered=True)

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
    def run_query_table_multi( self, search, and_flag=False ):
        psearch = search.copy()
        if and_flag is True:
            combo = " and "
        else:
            combo = " or  "
        conn = self.init_db()
        
            # Get Cursor
        cur = conn.cursor(buffered=True)

        my_sql_qry = "SELECT rec_id, title, http from recipe where"
        field = "title"

        q_bld = self.build_query(field, psearch, combo)
       

        print( "my_sql_qry: ", my_sql_qry + q_bld)
        print( "q_bld: ", q_bld)


        try:
            cur.execute(my_sql_qry + q_bld)          
        except mariadb.Error as e:
            print(f"Error: {e}")
            return None
        rowcount = cur.rowcount
        print("rowcnt:", rowcount)
        if rowcount == 0:
            print("no reesutls from query")

        #for item in cur:
        #    print(item)
        rtn_list = [x for x in cur]
        conn.close()
        return rtn_list

    def build_query(self,  field, psearch, combo):
        like_field = "( " + field + " like " 
        q_bld = ""
        psearch = list(filter(None,psearch))
        print("qsearch: ", psearch)
        while len(psearch) > 0:
            item = psearch.pop()
            if len(item) < 1:
                continue
            if len(psearch) > 0:
                q_bld =  q_bld + like_field +   "'%" + item + "%'" + ")" + combo 
            else:
                q_bld =  q_bld  + like_field   +  "'%" + item + "%'" ")"
        return q_bld

    def run_query_table_ing_multi( self, search, and_flag=False ):
        psearch = search.copy()
        if and_flag is True:
            combo = " and "
        else:
            combo = " or  "
        conn = self.init_db()

            # Get Cursor
        cur = conn.cursor(buffered=True)
        my_sql_qry = "SELECT rec_id, title, http from recipe where"
        field = "ingredients"
        q_bld = self.build_query(field, psearch, combo)

    
        print( "my_sql_qry: ", my_sql_qry + q_bld)
        print( "q_bld: ", q_bld)


        try:
            cur.execute(my_sql_qry + q_bld) 
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

    def run_query_table_category_multi( self, search, and_flag=False ):
        psearch = search.copy()
        if and_flag is True:
            combo = " and "
        else:
            combo = " or  "
        conn = self.init_db()

            # Get Cursor
        cur = conn.cursor(buffered=True)
        my_sql_qry = "SELECT rec_id, title, http from recipe where"
        field = "category"
        q_bld = self.build_query(field, psearch, combo)

    
        print( "my_sql_qry: ", my_sql_qry + q_bld)
        print( "q_bld: ", q_bld)


        try:
            cur.execute(my_sql_qry + q_bld) 
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

    def run_query_category_labels( self, search, and_flag=False ):
        # returns categories
        psearch = search.copy()
        if and_flag is True:
            combo = " and "
        else:
            combo = " or  "
        conn = self.init_db()

            # Get Cursor
        cur = conn.cursor(buffered=True)
        my_sql_qry = "SELECT rec_id, title, category from recipe where"
        field = "category"
        q_bld = self.build_query(field, psearch, combo)

    
        print( "my_sql_qry: ", my_sql_qry + q_bld)
        print( "q_bld: ", q_bld)


        try:
            cur.execute(my_sql_qry + q_bld) 
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

    def init_db(self):
        try:
                conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
                autocommit=True
                )
        except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}", e)
                sys.exit(1)
        return conn
            




if __name__ == "__main__":
    
    my_db = martha_db(load_var('DB_USERNAME'), load_var('DB_PASSWORD'))    
    
    res = my_db.run_query(13)
    print(res)


    res = my_db.run_query_table("Ham")

    print(res)

    res = my_db.run_query_table_multi(["Ham", "Cheese"], True)

    print(res)

    res = my_db.run_query_table_multi(["Ham", "Cheese", "Grill", "goat"], True)

    print(res)

    res = my_db.run_query_table_ing_multi(["Ginger", "flour"], True)

    print(res)

    status =  my_db.update_rec("13", "created", "2020-04-01")

    print(status)
