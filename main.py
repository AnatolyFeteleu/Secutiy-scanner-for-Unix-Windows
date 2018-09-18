from sqlite3 import IntegrityError
import os
import sys
import importlib
import json
import getpass
import datetime
import time
from scripts import Script001


sys.path.append(r'scripts' % getpass.getuser())
db = importlib.import_module('get_db')
test_script_0 = importlib.import_module('000test_file_exists')
test_script_1 = importlib.import_module('001test_script')


def create_tables():
    statement = "CREATE TABLE IF NOT EXISTS ControlTable (id_control INTEGER PRIMARY KEY, control TEXT, description TEXT, fix TEXT, checks TEXT, UNIQUE(control));"
    db.query(statement)
    statement = "CREATE TABLE IF NOT EXISTS ScanDataTable (id INTEGER PRIMARY KEY, id_control INTEGER, status TEXT, date_ TEXT, duration TEXT)"
    db.query(statement)
    statement = "CREATE TABLE IF NOT EXISTS AuditTable (id INTEGER PRIMARY KEY, attribute TEXT, value TEXT, UNIQUE (attribute))"
    db.query(statement)
    statement = "CREATE TABLE IF NOT EXISTS NetworkInterfaceTable (id INTEGER PRIMARY KEY, name TEXT, UNIQUE (name))"
    db.query(statement)


def get_scripts():
    script_list = []
    for i in os.listdir('%s\\scripts' % os.getcwd()):
        script_list.append(i)
    return script_list


def add_control(control=None, description=None, fix=None, checks=None):
    with open(r'C:\Users\%s\PycharmProjects\Positive\Positive-Technologies\control.json' % getpass.getuser()) as file:
        data = json.load(file)
        for id_control, col_2, col_3, col_4, col_5 in data:
            # statement = "INSERT OR IGNORE INTO ControlTable(title, target, description) VALUES (?, ?, ?)"
            statement = "INSERT INTO ControlTable(control, description, fix, checks) VALUES (?, ?, ?, ?)"
            try:
                if (control and description and fix and checks) != None:
                    return db.query(statement, (control, description, fix, checks))
                else:
                    db.query(statement, (col_2.encode('Windows-1251'), col_3.encode('Windows-1251'), col_4.encode('Windows-1251'), col_5.encode('Windows-1251')))
            except IntegrityError:
                raise NameError('Values is not unique')


def add_record(id_control, duration, date_=datetime.date.fromtimestamp(time.time()), status=None):
    statement = "INSERT INTO ScanDataTable (id_control, status, date_, duration) VALUES (?, ?, ?, ?)"
    if not status:
        raise NameError('Unknown status')
    else:
        return db.query(statement, (id_control, status[0], date_, duration))


def add_details_pc(obj):
    statement = "INSERT INTO AuditTable (attribute, value) VALUES (?, ?)"
    for i in obj:
        for j, k in zip(i.keys(), i.values()):
            try:
                db.query(statement, (j, k))
            except IntegrityError:
                raise NameError('Values is not unique')


def main():
    create_tables()
    add_control()
    # for i in get_scripts():
    #    if i[-3:] == '.py' and i[0:3] != 'get':
    #        importlib.import_module(i[:-3]).main()
    dummy = Script001.TransportSQL('mariadb')
    dummy.sql_exec("show databases")
    dummy.check_table('xxx')
    dummy.check_db("mariadb_3")
    add_record(id_control=1, status=test_script_0.main('/etc/test/myfile.txt'),
               duration=test_script_0.main('/etc/test/myfile.txt')[1])
    dummy = Script001.TransportWMI(ip='192.168.1.23')
    add_details_pc(dummy.wmi_query())
    path = r'Software\Microsoft\Windows\CurrentVersion\Policies\System'
    values = ['EnableLUA', 'EnableInstallerDetection', 'PromptOnSecureDesktop', 'EnableSecureUIAPaths',
              'EnableVirtualization', 'FilterAdministratorToken']
    for value, control in zip(values, range(2, 9)):
        add_record(id_control=control, status=test_script_1.main(ip='192.168.1.23', path=path, value=value),
                   duration=test_script_1.main(ip='192.168.1.23', path=path, value=value)[1])


if __name__ == '__main__':
    main()
