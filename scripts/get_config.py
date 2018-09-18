import os
import json
import settings


_config = None


def config():
    if os.path.isfile(r'%s\env.json' % settings.BASE_DIR):
        with open(r'%s\env.json' % settings.BASE_DIR) as file:
            global _config
            _config = json.load(file)
            return _config
    else:
        raise NameError('Config-file is not found')


if __name__ == '__main__':
    config()