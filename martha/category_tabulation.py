from ast import Return
from textblob import TextBlob
from marth_db import *
from load_var import * 

test_text = "Preheat a 5-to-6-quart slow cooker. Season lamb with salt and pepper. In a large Dutch oven, heat oil over medium-high. Add lamb and cook until golden brown all over, about 8 minutes. Transfer to slow cooker."
def new_func(m_text):
    print(m_text.tags)
    print(m_text.noun_phrases)
    print(m_text.sentiment)
    print(m_text.words)
    print(m_text.sentences)



def get_nouns( sentence_text ):
    m_text = TextBlob( sentence_text)

    tag_list = m_text.tags

    while len(tag_list) > 0:
        t_item = tag_list.pop()
        if t_item[1].startswith("NN"):
            yield t_item[0]

def insert_dict( word, dict):
    if word in dict:
        dict[word] += 1
    else:
        dict[word] = 1
    return
def get_categories_from_db():
    my_db = martha_db(load_var('DB_USERNAME'), load_var('DB_PASSWORD'))
    res = my_db.run_query_category_labels( ["%%"])
    return res

def main_loop():
    title_dict = {}
    res_list = get_categories_from_db()

    for r in res_list:
        #for t in get_nouns(r[2]):
        insert_dict( r[2], title_dict)

    for w in title_dict:
        if title_dict[w] > 2:
            print(( w + ":  " + str( title_dict[w])) )
        


if __name__ == "__main__":
 
    main_loop()
