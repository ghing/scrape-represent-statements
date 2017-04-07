import datetime

from sqlalchemy import (Column, Date, DateTime, Integer, String,
    UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Statement(Base):
    __tablename__ = 'statements'

    id = Column(Integer, primary_key=True)
    member = Column(String)
    member_url = Column(String)
    party = Column(String)
    state = Column(String)
    district = Column(String)
    date = Column(Date)
    title = Column(String)
    url = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            'member',
            'party',
            'state',
            'district',
            'date',
            'url'
        ),
    )

    def __repr__(self):
        return "<Statement(member='{}', member_url='{}', party='{}', state='{}' district='{}', date='{}', title='{}', url='{}')>".format(
             self.member, self.member_url, self.party, self.state,
             self.district, self.date, self.title, self.url)
