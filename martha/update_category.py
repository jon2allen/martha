import multiprocessing as mp
from datetime import datetime
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from marth_db import *
from load_var import *


def partition(lst, size):
    for i in range(0, len(lst), size):
        print("i: ", i )
        if ( i + size > len(lst )):
           yield lst[i:]
        else:
           yield lst[i : i+size]

def split_list( o_list, n ): 
    p_list = list(partition(o_list, n))
    return p_list

def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    try:
        req = requests.get(url)
    except:
        return None
    if req.status_code == 404:
        return None
    soup = BeautifulSoup(req.text, parser)
    return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

def get_category_from_http( url ):
    d = get_ld_json( url )
    if d is None:
        return None
    try:
        data1 = d[1]
    except:
        print("json error - bypass")
        return
    try:
        print( "categories: ", data1['recipeCategory'][0])

        cat = data1['recipeCategory']
    except:
        return
    return cat 

def get_date_from_http( url ):
    d = get_ld_json( url )
    if d is None:
        return None
    try:
        data1 = d[1]
    except:
        print("json error - bypass")
        return
    try:
        print( "Date published: ", str(data1['datePublished']))

        dt = parser.parse(data1['datePublished'])
    except:
        return
    return dt

def update_date_field( rec_id, http_dt):
    my_db = martha_db(load_var('DB_USERNAME'), load_var('DB_PASSWORD'))

    my_db.update_rec(rec_id, "created", datetime.strftime(http_dt, '%Y-%m-%d'))
    print( "created updaated", datetime.strftime(http_dt, '%Y-%m-%d'))
    return

def update_category_field( rec_id, category ):
    cat_list = category[0].split()
    cat_word = cat_list[0]
    my_db = martha_db(load_var('DB_USERNAME'), load_var('DB_PASSWORD'))

    my_db.update_rec(rec_id, "category", cat_word.lower())
    print( "category updaated: ", cat_word)
    return

def process_update_from_http( res ):
    x=0
#    print( "res: ", res )
    for r in res:
       x = x+1
       http_url = r[2]
       print ( "rec_id: ", r[0])
       print ( "http_url: ", http_url )
       categories = get_category_from_http( http_url)
       if categories is None:
           print(' no date from http')
           continue
       update_category_field( r[0], categories)
       # set a limit to how many to do.
       #if x > 2:
       #   break



def main_loop():
    my_db = martha_db(load_var('DB_USERNAME'), load_var('DB_PASSWORD'))

    res = my_db.run_query_get_all()
    print("type: ",  type(res) )
    print("res: ", len(res), "div by 12: ", (len(res)/12) )
    lst_4_part = split_list( res, 6200 )
    print( len(lst_4_part))
    print( len(lst_4_part[0] ))
    print( len(lst_4_part[1] ))
    print( len(lst_4_part[2] ))
    print( len(lst_4_part[3] ))
    new_lst = (lst_4_part[0], lst_4_part[1],lst_4_part[2],lst_4_part[3])
    mp.set_start_method('spawn')
    with mp.Pool(4) as pool:
        pool.map(process_update_from_http, lst_4_part, 1)
    #process_update_from_http( lst_4_part[3] )


if __name__ == "__main__":
    main_loop()
