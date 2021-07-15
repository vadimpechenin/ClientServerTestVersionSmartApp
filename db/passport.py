"""
Сущность из БД - пасспорт детали passport
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class Passport(Base):
    __tablename__ = 'passport'
    passport_id = sa.Column(sa.Integer(), primary_key=True)
    type_id = sa.Column(sa.Integer, sa.ForeignKey('type.type_id'), nullable=False)
    location_id = sa.Column(sa.Integer, sa.ForeignKey('location.location_id'), nullable=False)
    # characteristic_id = Column(Integer, ForeignKey('characteristic.id'), nullable=False)
    receipt_date = sa.Column(sa.DateTime)
    characteristic = relationship('Characteristic', backref='passport', uselist=False)  # one to one

    def __repr__(self):
        # для печати строки и отладки
        return '<Characteristics[type_id="{}", location_id="{}", receipt_date="{}"]>'.format(
            self.type_id, self.location_id, self.characteristics_id, self.receipt_date)