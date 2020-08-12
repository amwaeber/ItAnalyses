import os
from configparser import ConfigParser

from itanalyses.utility.version import __version__

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

global_confs = {'progname': 'ItAnalyses',
                'progversion': __version__}
paths = {'icons': os.path.join(PROJECT_PATH, 'icons'),
         'last_index': PROJECT_PATH,
         'last_plot_save': PROJECT_PATH,
         'last_analysis': PROJECT_PATH,
         'last_export': PROJECT_PATH
         }


def read_config():
    if not os.path.exists(os.path.join(PROJECT_PATH, 'config.ini')):
        write_config()
    config = ConfigParser()
    config.read(os.path.join(PROJECT_PATH, 'config.ini'))

    for key in config['globals']:
        global_confs[key] = str(config['globals'][key])

    for key in config['paths']:
        paths[key] = str(config['paths'][key])


def write_config(**kwargs):
    config_path = os.path.join(PROJECT_PATH, 'config.ini')

    config = ConfigParser()

    config['globals'] = {'progname': 'ItAnalyses',
                         'progversion': __version__
                         }

    config['paths'] = {'icons': paths['icons'],
                       'last_index': kwargs.get('index_path', paths['last_index']),
                       'last_plot_save': kwargs.get('plot_path', paths['last_plot_save']),
                       'last_analysis': kwargs.get('analysis_path', paths['last_analysis']),
                       'last_export': kwargs.get('export_path', paths['last_export'])
                       }

    with open(config_path, 'w') as f:
        config.write(f)
