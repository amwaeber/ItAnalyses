import datetime
import pandas as pd

from itanalyses.data.parameters.info import info_pars


def save_info(file_path='.', **kwargs):

    defaults = [['N/A'], [datetime.date(1970, 1, 1)], ['unknown'], [datetime.date(1970, 1, 1)], [-1], [-1],
                ['unknown'], ['unknown'], [-1], [-1], ['unknown'], ['unknown'], ['unknown'], [-1], ['unknown'],
                [datetime.date(1970, 1, 1)], [-1], [-1], [-1], [-1]]

    df = pd.DataFrame({par: kwargs.get(par, defaults[i]) for i, par in enumerate(info_pars)})
    df.to_csv(file_path)
