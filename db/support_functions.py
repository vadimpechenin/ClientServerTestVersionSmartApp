"""
Вспомогательные функции, собранные для разных классов
"""

def resultproxy_to_dict(s2):
    # Функция сохранения результатов запроса в словарь
    d, a = {}, []
    for rowproxy in s2:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return a