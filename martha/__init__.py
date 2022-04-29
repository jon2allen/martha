import os

from datetime import timedelta

from flask import Flask

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# from martha.select_query import *
from martha.marth_db import *

from flask_session import Session

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    try:
       app.config['DB_USERNAME']=os.environ['DB_USERNAME']
       app.config['DB_PASSWORD']=os.environ['DB_PASSWORD']
    except:
       print("error:  Username and Password env not set")
       exit(8)

    sess = Session()
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    sess.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # search = Blueprint('search', __name__, url_prefix='/search')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/mainpage')
    def display_main():
        return render_template('main.html')

    @app.route('/displayrec1', methods=['GET','POST'])
    def display_rec1():
        if session["results"]:
            myres = session["results"]
            # print("myres:" , myres[0])
        rec_id = request.args.get('item') 
        print( "rec_id:",  rec_id)
        db1 = martha_db( app.config['DB_USERNAME'], app.config['DB_PASSWORD'])
        recipe = db1.run_query( rec_id )
        # print(recipe)
        if recipe == None:
             return "Invalid rec_id: " + rec_id
        else:
             return render_template('recipe.html', recipe=recipe)

    @app.route('/search', methods = ['GET', 'POST'])
    def table_search():
        if request.method == 'GET':
            print("Request: GET")
        if request.method == 'POST':
            keyword = request.form['keyword']
            db1 = martha_db( app.config['DB_USERNAME'], app.config['DB_PASSWORD'])
            results = db1.run_query_table( keyword )
            return render_template('rec_table.html', results=results,
             num_results=len(results))
        else:
            return render_template('title_search.html')

    @app.route('/searchTitle', methods = ['GET', 'POST'])
    def table_search_title_many():
        if request.method == 'GET':
            print("Request: GET")
            if "and_sel" in request.args:
                 title_list = [ request.args.get('keyword1'), 
                 request.args.get('keyword2'),
                 request.args.get('keyword3') ]
                 and_value = request.args.get('and_sel')
                 print("t", title_list)
            else:
                return render_template('title_search_multi.html')
        if request.method == 'POST':
            print(request.form)
            title_list = [ request.form["keyword1"], 
                request.form["keyword2"],
                request.form["keyword3"]]
            and_value = request.form["and_sel"]
        and_flag = True
        if request.form["and_sel"] == "or_sel":
            and_flag = False
        ksearch = title_list
        print(" here at db ")
        db1 = martha_db( app.config['DB_USERNAME'], app.config['DB_PASSWORD'])
        # print("password: ", app.config['DB_PASSWORD'] )
        res = db1.run_query_table_multi(title_list, and_flag)
        session["results"] = res
        session["ksearch"] = ksearch
        session["and_value"] = and_value
        return render_template('rec_table2.html', results=res, 
        num_results=len(res),
        ksearch=ksearch)

    

    @app.route('/searchIngredients', methods = ['GET', 'POST'])
    def table_search_ingredient_many():
        if request.method == 'GET':
            print("Request: GET")
            if "and_sel" in request.args:
                 title_list = [ request.args.get('keyword1'), 
                 request.args.get('keyword2'),
                 request.args.get('keyword3') ]
                 and_value = request.args.get('and_sel')
                 print("t", title_list)
            else:
                return render_template('ingredient_search.html')
        if request.method == 'POST':
            print(request.form)
            title_list = [ request.form["keyword1"], 
                request.form["keyword2"],
                request.form["keyword3"], ]
            and_flag = True
            if request.form["and_sel"] == "or_sel":
                and_flag = False
            and_value = request.form["and_sel"]
            db1 = martha_db( app.config['DB_USERNAME'],app.config['DB_PASSWORD'])
            res = db1.run_query_table_ing_multi(title_list, and_flag)
            ksearch = title_list
            session["results"] = res
            session["ksearch"] = ksearch
            session["and_value"] = and_value
            return render_template('rec_table2.html', results=res, 
            num_results=len(res),
            ksearch=title_list)


    return app
