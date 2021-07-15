"""
Файл __init__.py позволяет каталогам Python обрабатывать их как модули.
Кроме того, это первый файл, который нужно загрузить в модуле,
поэтому вы можете использовать его для выполнения кода, который вы хотите запускать
каждый раз при загрузке модуля, или указать подмодули, которые будут экспортированы.
"""

from .base import Session, current_session
from .characteristic import Characteristic
from .type import Type
from .location import Location
from .passport import Passport