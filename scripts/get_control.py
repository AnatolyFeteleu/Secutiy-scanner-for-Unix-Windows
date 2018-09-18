import os
import json
import settings


_control = None


def control():
    if os.path.isfile(r'%s\control.json' % settings.BASE_DIR):
        with open(r'%s\control.json' % settings.BASE_DIR) as file:
            global _control
            _control = json.load(file)
            return _control
    else:
        raise NameError('Control-file is not found')


if __name__ == '__main__':
    control()
