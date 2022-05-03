import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from dateutil import parser

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


if __name__ == "__main__":
    #d = get_ld_json(  "https://www.marthastewart.com/1517366/cherry-and-cream-cheese-hand-pies")
    
    d = get_ld_json(  "https://www.marthastewart.com/1511151/zarape-de-pato")
    #d = get_ld_json(  " https://www.marthastewart.com/265389/jingle-bell-ponytail-holders")
    if d is None:
        print("request failed")
    pprint(d[1])

    print ("-----")
    for i in d:
        print("list item ---")
      #  pprint(i)

    data1 = d[1]

    print( "Date published: ", data1['datePublished'])

    dt = parser.parse(data1['datePublished'])

    print(type(dt))

    print( dt.year)
    print( dt.month)

   # print("\n\n Date Published: ", d['datePublished'] )

    instructions = data1['recipeIngredient']

    for i in instructions:
       print(i)

    directions = data1['recipeInstructions']

    count = 0
    for d in directions:
       count += 1
       print(" " + str(count) + ":  " + d['text'])



