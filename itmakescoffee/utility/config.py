import os
from configparser import ConfigParser

from itmakescoffee.utility.version import __version__

PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../itmakescoffee/..')

global_confs = {}
paths = {}
ports = {}


def read_config():
    if not os.path.exists(os.path.join(PROJECT_PATH, 'config.ini')):
        write_config()
    config = ConfigParser()
    config.read(os.path.join(PROJECT_PATH, 'config.ini'))

    for key in config['globals']:
        global_confs[key] = str(config['globals'][key])

    for key in config['paths']:
        paths[key] = str(config['paths'][key])

    for key in config['ports']:
        ports[key] = str(config['ports'][key])


def write_config(**kwargs):
    config_path = os.path.join(PROJECT_PATH, 'config.ini')

    config = ConfigParser()

    config['globals'] = {'progname': 'ItMakesCoffee',
                         'progversion': __version__
                         }

    config['paths'] = {'icons': os.path.join(PROJECT_PATH, 'icons'),
                       'last_save': kwargs.get('save_path', PROJECT_PATH),
                       'last_plot_save': kwargs.get('plot_path', PROJECT_PATH),
                       'last_analysis': kwargs.get('analysis_path', PROJECT_PATH),
                       'last_export': kwargs.get('export_path', PROJECT_PATH)
                       }

    config['ports'] = {'arduino': kwargs.get('arduino', 'dummy'),
                       'keithley': kwargs.get('keithley', 'dummy')
                       }

    with open(config_path, 'w') as f:
        config.write(f)
