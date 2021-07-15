"""
Сущность из БД - номенклатура деталей type
"""
import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class Type(Base):
    __tablename__ = 'type'
    type_id = sa.Column(sa.Integer(), primary_key=True)
    type_name = sa.Column(sa.String)
    passport = relationship('Passport', backref='type', lazy=True)  # one to many

    def __repr__(self):
        # для печати строки и отладки
        return '<Type[type_name="{}"]>'.format(self.type_name)