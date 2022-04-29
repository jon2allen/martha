from datetime import datetime
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from marth_db import *
from load_var import *

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
        print( "Date published: ", data1['datePublished'])

        dt = parser.parse(data1['datePublished'])
    except:
        return
    return dt

def update_date_field( rec_id, http_dt):
    my_db = martha_db(load_var('DB_USERNAME'), load_var('DB_PASSWORD'))

    my_db.update_rec(rec_id, "created", datetime.strftime(http_dt, '%Y-%m-%d'))
    print( "created updaated", datetime.strftime(http_dt, '%Y-%m-%d'))
    return
def main_loop():
    my_db = martha_db(load_var('DB_USERNAME'), load_var('DB_PASSWORD'))

    res = my_db.run_query_get_all()
    x = 0
    for r in res:
        x = x+1
        http_url = r[2]
        print ( "rec_id: ", r[0])
        print ( "http_url: ", http_url )
        http_dt = get_date_from_http( http_url) 
        if http_dt is None:
            print(' no date from http')
            continue 
        update_date_field( r[0], http_dt)    
        # set a limit to how many to do. 
        if x > 2:
            break


if __name__ == "__main__":
    main_loop()
