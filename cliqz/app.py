from flask import Flask
from cfg import SQL_URI_WEBAPP, MEDIA_PATH
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.wsgi import SharedDataMiddleware


app = Flask(__name__)
engine = create_engine(SQL_URI_WEBAPP, convert_unicode=True, pool_size=50, max_overflow=50, pool_timeout=5,
                       pool_recycle=3600)
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))
Base = declarative_base()
Base.query = db.query_property()
app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                    {'/media/': MEDIA_PATH})
app.jinja_env.cache = None