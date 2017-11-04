"""Database creator."""

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime
)

from .meta import Base
from datetime import datetime


class Entry(Base):
    """Create table and rows."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    creation_date = Column(DateTime)
    body = Column(Unicode)

    def __init__(self, *args, **kwargs):
        """Modify the init method to do more things."""
        super(Entry, self).__init__(*args, **kwargs)
        self.creation_date = datetime.now()
