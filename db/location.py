"""
Сущность из БД - месторасположение детали location
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class Location(Base):
    __tablename__ = 'location'
    location_id = sa.Column(sa.Integer(), primary_key=True)
    workshop_number = sa.Column(sa.String)
    lot_number = sa.Column(sa.String)
    passport1 = relationship('Passport', backref='location', lazy=True)  # one to many

    def __repr__(self):
        # для печати строки и отладки
        return '<Location[workshop_number="{}", lot_number="{}"]>'.format(self.workshop_number, self.lot_number)