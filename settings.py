import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DB_NAME = BASE_DIR + '\\scripts\\' + 'database.db'

STATUSES = {1: 'STATUS_COMPLIANT', 2: 'STATUS_NOT_COMPLIANT', 3: 'STATUS_NOT_APPLICABLE', 4: 'STATUS_ERROR',
            5: 'STATUS_EXCEPTION'}

WMI_KEYS = dict(HCR='2147483648', HCU='2147483649', HKLM='2147483650', HU='2147483651', HCC='2147483653',
                HDD='2147483654')