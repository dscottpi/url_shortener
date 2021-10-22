__version__ = '0.1.0'

import os
import re

from flask import Flask, redirect, abort, request, render_template

from app.db import get_db
from app.id_generator import Snowflake
from app.base62 import encode

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'url_shortener.sqlite'),
    )

    snowflake = Snowflake()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/<string:short_url>', methods=('GET',))
    def get_long_url(short_url: str):
        db = get_db()
        url = db.execute('SELECT long_url from url where short_url = ?', ((short_url,))).fetchone()
        if url is None:
            abort(400)

        return redirect(url['long_url'], code=301)

    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.))+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
        r'localhost|' 
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    @app.route('/', methods=('POST', 'GET'))
    def index():
        if request.method == "POST":
            long_url = request.form['long_url']
            if regex.match(long_url) is None:
                abort(400)

            db = get_db()
            url = db.execute('SELECT * from url where long_url = ?', ((long_url,))).fetchone()
            if url is not None:
                return render_template('index.html', short_url=url['short_url'])

            id =  snowflake.mint_id()
            short_url = encode(id)

            db.execute('INSERT INTO url (id, short_url, long_url) values (?, ?, ?)', (id, short_url, long_url))
            db.commit()

            return render_template('index.html', short_url=short_url)

        return render_template('index.html')
        
    
    from . import db
    db.init_app(app)

    return app