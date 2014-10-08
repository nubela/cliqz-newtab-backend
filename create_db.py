from cliqz.app import engine
from cliqz.model import Base


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()
