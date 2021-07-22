"""
Вспомогательные функции, собранные для разных классов
"""

def resultproxy_to_dict(s2):
    # Функция сохранения результатов запроса в словарь
    d, a = {}, []
    for rowproxy in s2:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        # for column, value in rowproxy.items():
        # Для SQLAlchemy 1.4.17
        k=0
        for column in rowproxy._fields:
            # build up the dictionary
            value = rowproxy._data[k]
            d = {**d, **{column: value}}
            k += 1
        a.append(d)
    return a

