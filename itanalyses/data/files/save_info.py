import pandas as pd

from itanalyses.data.parameters.info import info_pars


def save_info(file_path='.', **kwargs):

    df = pd.DataFrame({par: kwargs.get(par, info_pars[par]) for par in info_pars})
    df.to_csv(file_path)
