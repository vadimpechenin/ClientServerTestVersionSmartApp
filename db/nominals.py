"""
Сущность из БД - номинальные значение для деталей + путь к изображениям деталей
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class Nominals(Base):
    __tablename__ = 'nominals'

    nominal_id = sa.Column(sa.Integer(), primary_key=True)
    type_id = sa.Column(sa.Integer, sa.ForeignKey('type.type_id'), nullable=False)
    path_to_image = sa.Column(sa.String)
    imbalance = sa.Column(sa.Float)
    tolerance_imbalance_lower = sa.Column(sa.Float)
    tolerance_imbalance_upper = sa.Column(sa.Float)
    diameter = sa.Column(sa.Float)
    tolerance_diameter_lower = sa.Column(sa.Float)
    tolerance_diameter_upper = sa.Column(sa.Float)
    type = relationship('Type', backref='nominals')

    def __repr__(self):
        # для печати строки и отладки
        return '<Nominals[imbalance="{}", diameter="{}"]>'.format(self.imbalance, self.diameter)