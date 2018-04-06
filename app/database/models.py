from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from app.database import Base


class Library(Base):
    __tablename__ = 'Libraries'

    _id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(20))
    location_road = Column('location_road', String(40))
    location_number = Column('location_number', String(20))
    location_detail = Column('location_detail', String(40))
    manager_name = Column('manager_name', String(20))
    manager_email = Column('manager_email', String(20))
    manager_phone = Column('manager_phone', String(20))
    audiences = Column('audiences', String(20))
    fac_beam_screen = Column('fac_beam_screen', TINYINT)
    fac_sound = Column('fac_sound', TINYINT)
    fac_record = Column('fac_record', TINYINT)
    fac_placard = Column('fac_placard', TINYINT)
    fac_self_promo = Column('fac_self_promo', TINYINT)
    fac_other = Column('fac_other', String(40))
    req_speaker = Column('req_speaker', String(40))
