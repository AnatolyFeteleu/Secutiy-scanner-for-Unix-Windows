from jinja2 import Environment, FileSystemLoader, select_autoescape
import importlib
import sqlite3
from collections import Counter
import settings
import re

script_001 = importlib.import_module('Script001')


def create_report():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['xml', 'html'])
    )
    configuration = importlib.import_module('get_config').config()  # Конфигурация подключения
    transport_name = list(configuration["transports"].keys())[0]
    connect = sqlite3.connect(r'%s\scripts\database.db' % settings.BASE_DIR)
    cursor = connect.cursor()

    statement = 'SELECT id, id_control, status, duration, date_  FROM ScanDataTable;'  # Общее количество проверок
    checking = cursor.execute(statement).fetchall()

    statement = 'SELECT id FROM ScanDataTable'
    num_inspects = len(cursor.execute(statement).fetchall())

    statement = 'SELECT status FROM ScanDataTable;'  # Группировка по статусам
    group_status = Counter(cursor.execute(statement).fetchall())
    groups = []
    for key, value in zip(dict(group_status).keys(), dict(group_status).values()):
        groups.append([key[0], value])

    statement = 'SELECT * FROM AuditTable;'
    os_info = cursor.execute(statement)
    os_list = []
    for i in os_info:
        os_list.append([i[1], i[2]])

    statement = 'SELECT * FROM ControlTable;'
    controls = cursor.execute(statement)
    control_list = list()
    control_list.append('')
    for i in controls:
        control_list.append(i)

    dummy = script_001.TransportSNMP()
    infos = list(dummy.get_information('interfaces').values())
    list_interfaces = []
    pattern = r'[A-Z]?[a-z]+[A-Z]?[a-z]+[\-]?[a-z]+'
    for i in infos:
        match = re.search(pattern, i)
        list_interfaces.append(match.group())
    count_interfaces = dict(Counter(list_interfaces))
    connect.close()

    template = env.get_template('index.html')
    #  rendered_template = template.render(checkings=checking, configuration=configuration, transport_name=transport_name,
    #                                      group_status=groups, control_list=control_list,
    #                                      num_inspects=num_inspects, system=os_list, interfaces=count_interfaces)
    #  print(rendered_template)

    test = importlib.import_module('get_control').control()
    print(test[1][2].encode('utf-8'))
    print(str(test[1][2].encode('Windows-1251'), 'utf-8'))


if __name__ == '__main__':
    create_report()

