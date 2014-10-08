from cliqz.app import Base
from cliqz.util import generate_uuid
from sqlalchemy import Column, Unicode, DateTime


class UnsplashImage(Base):
    __tablename__ = 'unsplash_images'
    id = Column(Unicode(255), primary_key=True)
    utc_date_created = Column(DateTime)
    filename = Column(Unicode(255))
    utc_expiry = Column(DateTime, nullable=True)

    def __init__(self):
        self.id = generate_uuid()