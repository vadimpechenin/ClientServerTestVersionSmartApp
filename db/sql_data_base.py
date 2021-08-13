"""
Класс для работы с базой данных
"""

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from db.support_functions import resultproxy_to_dict

from .base import Session, current_session, Base
from .characteristic import Characteristic
from .type import Type
from .location import Location
from .passport import Passport
from .nominals import Nominals


class SQL_data_base():

    def __init__(self,id,pl_table,imbalance_tolerance):
        self.id = id
        self.engine = create_engine('sqlite:///smart_warehouse.db', echo = True)
        self.pl_table = pl_table
        self.imbalance_tolerance= imbalance_tolerance



    def table_create(self):
        #Метод для создания таблиц и базы данных
       Base.metadata.create_all(self.engine)

    def create_session(self):
        #Создание сессии, через которую мапяться объекты
        self.session = sessionmaker(bind=self.engine)()

    def init_repletion_data_base(self):
        # Создание объектов в таблице Type
        names_list = ['Деталь 1', 'Деталь 2', 'Деталь 3', 'Деталь 4', 'Деталь 5', 'Деталь 6']

        if (self.pl_table[1] == 1):
            # Добавать в сессию
            for name in names_list:
                type_object = Type(type_name=name)
                self.session.add(type_object)
            self.session.commit()

        # Создание объектов в таблице Location
        workshop_list = ['1', '2', '3', '4', '5', '6']
        lot_list = ['1', '2', '3']
        if (self.pl_table[2] == 1):
            # Добавать в сессию
            for workshop in workshop_list:
                for lot in lot_list:
                    location_object = Location(workshop_number=workshop, lot_number=lot)
                    self.session.add(location_object)
            self.session.commit()

        # Создание объектов в таблице Passport
        import random
        from datetime import datetime
        from datetime import timedelta
        def random_date(start, end):
            """
            This function will return a random datetime between two datetime
            objects.
            """
            delta = end - start
            int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
            random_second = random.randrange(int_delta)
            return start + timedelta(seconds=random_second)

        d1 = datetime.strptime('1/1/2020 1:30:40 PM', '%m/%d/%Y %I:%M:%S %p')
        d2 = datetime.strptime('6/30/2021 4:50:50 AM', '%m/%d/%Y %I:%M:%S %p')
        if (self.pl_table[3] == 1):
            # Добавать в сессию
            for i in range(30):
                type_id = random.randint(1, len(names_list))
                location_id = random.randint(1, len(workshop_list) * len(lot_list))
                date = random_date(d1, d2)
                passport_object = Passport(type_id=type_id, location_id=location_id, receipt_date=date)
                self.session.add(passport_object)
            self.session.commit()

        # Создание объектов в таблице Characteristic
        passport_id_list = [1, 2, 5, 7, 8, 10, 12, 14, 17, 18, 20, 24, 27, 28, 29, 30]
        if (self.pl_table[4] == 1):
            # Добавать в сессию
            for passport_id in passport_id_list:
                imbalance = random.random() * 5
                diameter = random.random() * 10
                characteristic_object = Characteristic(passport_id=passport_id, imbalance=imbalance, diameter=diameter)
                self.session.add(characteristic_object)
            self.session.commit()

        # Создание объектов в таблице Nominals
        type_id_list = [1, 2, 3, 4, 5, 6]
        if (self.pl_table[4] == 1):
            # Добавать в сессию
            k = 1
            for type_id in type_id_list:
                path_to_image = 'D:\\PYTHON\\Programms\\Smart_app_UMNIK\\Photos_of_details\\' + str(k) + '.jpg'
                imbalance = 0
                tolerance_imbalance_lower = 0
                tolerance_imbalance_upper = 1 + random.random() * 2
                diameter = 5
                tolerance_diameter_lower = -2 + random.random()
                tolerance_diameter_upper = 1 + random.random()
                nominal_object = Nominals(type_id=type_id, path_to_image=path_to_image,
                                                       imbalance=imbalance, tolerance_imbalance_lower=tolerance_imbalance_lower,
                                                       tolerance_imbalance_upper=tolerance_imbalance_upper, diameter=diameter,
                                                       tolerance_diameter_lower=tolerance_diameter_lower,
                                                       tolerance_diameter_upper=tolerance_diameter_upper)
                self.session.add(nominal_object)
                k += 1
            self.session.commit()

    def request_of_imbalance(self):
        # Функция для подачи запроса
        request_str = "SELECT passport.passport_id, imbalance, diameter \
                           FROM \
                           passport INNER JOIN characteristic \
                           ON passport.passport_id=characteristic.passport_id \
                           WHERE imbalance<" + str(self.imbalance_tolerance) +" \
                           ORDER BY diameter DESC;"
        s2 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s2)
        return result_of_query

    def search_for_id(self, id):
        # Функция для подачи запроса на поиск
        request_str = "SELECT type_name \
                              FROM \
                              type INNER JOIN passport \
                              ON type.type_id=passport.type_id \
                              WHERE passport.passport_id=" + str(id)
        s2 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s2)
        return result_of_query

    def updata_for_id(self, id, datetime_noSQL, workshop, lot):
        # Функция для подачи запроса на поиск
        from datetime import datetime
        d1 = datetime.strptime('1/1/2020 1:30:40 PM', '%m/%d/%Y %I:%M:%S %p')
        data_time = ''
        k = 0
        for j in datetime_noSQL:
            if (j == '_') and (k <2):
                data_time = data_time + '/'
                k+=1
            elif (j == '_') and ((k ==2) or (k ==5)):
                data_time = data_time + ' '
                k+=1
            elif (j == '_') and ((k ==3) or (k==4)):
                data_time = data_time + ':'
                k+=1
            else:
                data_time = data_time + j

        data_time_for_recording = datetime.strptime(data_time, '%m/%d/%Y %I:%M:%S %p')
        #r = str(data_time_for_recording)
        # Поиск id расположения детали
        request_str = "SELECT location_id \
                        FROM location \
                        WHERE workshop_number = " + workshop + " AND lot_number = " + lot
        s2 = self.session.execute(request_str)
        result_id_location = resultproxy_to_dict(s2)

        request_str = "UPDATE passport \
                        SET receipt_date = '" + str(data_time_for_recording) + "',\
                        location_id = " + str(result_id_location[0]['location_id']) + "\
                        WHERE passport.passport_id=" + str(id)
        self.session.execute(request_str)

        result_of_query = 'Запись по детале с id =' + str(id) + ' изменена'
        #result_of_query = resultproxy_to_dict(s2)
        return result_of_query

    def list_of_parts(self):
        # Вызов списка видов деталей из базы данных
        request_str = "SELECT type_name \
                                      FROM \
                                      type;"
        s4 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s4)
        ciphers = []
        for a1 in result_of_query:
            #print(a1)
            ciphers.append(a1['type_name'])
        return ciphers

    def list_of_workshop_lot(self):
        # Вызов списка возможных мест расположений деталей
        request_str = "SELECT workshop_number, lot_number \
                                      FROM \
                                      location;"
        s4 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s4)
        ciphers = []
        for a1 in result_of_query:
            #print(a1)
            ciphers.append([a1['workshop_number'], a1['lot_number']])
        return ciphers

    def list_of_characteristics(self):
        #Список геометрических параметров из базы данных
        request_str = "SELECT imbalance, diameter \
                                             FROM \
                                             characteristic;"
        s4 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s4)
        ciphers = []
        for a1 in result_of_query:
            # print(a1)
            ciphers.append([a1['imbalance'], a1['diameter']])
        return ciphers

    def all_lists_for_filter(self):
        #Последовательный вызов всех списков характеристик из базы данных
        result_request=[]
        r = self.list_of_parts()
        result_request.append(self.list_of_parts())
        result_request.append(self.list_of_workshop_lot())
        result_request.append(self.list_of_characteristics())
        return result_request

    def data_for_report(self,parameters):
        # Финальный список для отчета по результатам фильтров

        #Формирование ограничений
        textstrType = ''
        for item in parameters.type_name_list:
            textstrType = textstrType + "'" +  item + "', "
        textstrType = textstrType.rstrip(', ')

        textstrWorkshop = ''
        for item in parameters.workshop_number_list:
            textstrWorkshop = textstrWorkshop + "'" + item + "', "
        textstrWorkshop = textstrWorkshop.rstrip(', ')
        textstrLot = ''
        for item in parameters.lot_number_list:
            textstrLot = textstrLot + "'" + item + "', "
        textstrLot = textstrLot.rstrip(', ')
        #Текст запроса
        request_str = "SELECT passport.passport_id, type.type_name, passport.receipt_date, location.workshop_number, \
                                location.lot_number, characteristic.imbalance, characteristic.diameter \
                        FROM type \
                        INNER JOIN passport USING(type_id) \
                        INNER JOIN location USING(location_id)\
                        LEFT JOIN characteristic on passport.passport_id=characteristic.passport_id\
                        WHERE type.type_name IN (" + str(textstrType) + ") AND  \
                              location.workshop_number IN (" + str(textstrWorkshop) + ") AND  \
                              location.lot_number IN (" + str(textstrLot) + ") AND  \
                              characteristic.imbalance>" + str(parameters.imbalance_list[0]) + " AND characteristic.imbalance<" + str(parameters.imbalance_list[1]) + " AND  \
                              characteristic.diameter > " + str(parameters.diameter_list[0]) + " AND characteristic.diameter < " + str(parameters.diameter_list[1]) + "\
                        ;"
        s4 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s4)
        ciphers = []
        for a1 in result_of_query:
            # print(a1)
            ciphers.append([a1['passport_id'], a1['type_name'], a1['receipt_date'], a1['workshop_number'], a1['lot_number'], a1['imbalance'], a1['diameter']])
        return ciphers

    def data_for_report_nomenclature(self,parameters):
        # Финальный список для определенного наименования деталей
        # Текст запроса
        request_str = "SELECT passport.passport_id,passport.receipt_date, location.workshop_number, \
                                       location.lot_number \
                               FROM type \
                               INNER JOIN passport USING(type_id) \
                               INNER JOIN location USING(location_id)\
                               WHERE type.type_name IN ('" + str(parameters.type_name) + "');"
        s4 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s4)
        ciphers = []
        for a1 in result_of_query:
            # print(a1)
            ciphers.append(
                [a1['passport_id'], a1['receipt_date'], a1['workshop_number'], a1['lot_number']])
        return ciphers

    def data_for_report_nomenclature2(self,parameters):
        # Финальный список конструкторских параметров для определенного наименования деталей
        # Текст запроса
        request_str = "SELECT path_to_image, imbalance, tolerance_imbalance_lower, tolerance_imbalance_upper, \
                                       diameter, tolerance_diameter_lower, tolerance_diameter_upper\
                               FROM type \
                               INNER JOIN nominals USING(type_id) \
                               WHERE type.type_name IN ('" + str(parameters.type_name) + "');"
        s4 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s4)
        ciphers = []
        for a1 in result_of_query:
            # print(a1)
            ciphers.append(
                [a1['path_to_image'], a1['imbalance'], a1['tolerance_imbalance_lower'], a1['tolerance_imbalance_upper'],
                 a1['diameter'], a1['tolerance_diameter_lower'], a1['tolerance_diameter_upper']])
        return ciphers