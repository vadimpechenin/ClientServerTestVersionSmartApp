"""
Сущность из БД - геометрические характеристики детали characteristic
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class Characteristic(Base):
    __tablename__ = 'characteristic'
    characteristic_id = sa.Column(sa.Integer(), primary_key=True)
    passport_id = sa.Column(sa.Integer, sa.ForeignKey('passport.passport_id'), nullable=False)
    imbalance = sa.Column(sa.Float)
    diameter = sa.Column(sa.Float)
    passport2 = relationship('Passport', backref='characteristics')

    def __repr__(self):
        # для печати строки и отладки
        return '<Characteristics[characteristics_id="{}", imbalance="{}", diameter="{}"]>'.format(
            self.characteristics_id, self.imbalance, self.diameter)