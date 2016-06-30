# -*- coding: utf-8 -*-
from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy



bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)
    
    
    import re
    from jinja2 import evalcontextfilter, Markup, escape

    @app.template_filter()
    @evalcontextfilter
    def nl2br(eval_ctx, value):
       _paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')
       result = u'\n\n'.join(u'<p>%s</p>' % p.replace(u'\r\n', u'<br/>') for p in _paragraph_re.split(value))
       if eval_ctx.autoescape:
           result = Markup(result)
       return result
    
    #environment.filters['nl2br'] = nl2br

    from .myriceprojects import myriceprojects as myriceprojects_blueprint
    app.register_blueprint(myriceprojects_blueprint)

    return app




