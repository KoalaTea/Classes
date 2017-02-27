from os.path import abspath, join, dirname

basedir = abspath(dirname(__file__))
configs_file = open(join(basedir,  'config.file'))

WTF_CSRF_ENABLED = True
SECRET_KEY = configs_file.readline().strip()

