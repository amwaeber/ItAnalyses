import pandas as pd


def average_results(data_list):
    if not data_list:  # return empty dataframe if empty list
        return pd.DataFrame()
    df = get_results(data_list)
    df_avg = df.groupby(["Experiment"]).agg({'Time': 'min',
                                             'Voc': ['mean', 'std'],
                                             'Isc': ['mean', 'std'],
                                             'MaxPower': ['mean', 'std'],
                                             'FillFactor': ['mean', 'std'],
                                             'Temperature': ['mean', 'std'],
                                             'Irradiance':['mean', 'std']})
    df_avg.columns = ["_".join(x) for x in df_avg.columns.ravel()]
    df_avg = df_avg.sort_values(by=['Time_min'])
    # if export:
    #     df_avg.rename(columns={"Timestamp_min": "Time (s)",
    #                            "MaxPower_mean": "Mean Pmax (W)",
    #                            "MaxPower_std": "Stdev Pmax (W)",
    #                            "Voc_mean": "Mean Voc (V)",
    #                            "Voc_std": "Stdev Voc (V)",
    #                            "Isc_mean": "Mean Isc (A)",
    #                            "Isc_std": "Stdev Isc (A)",
    #                            "FillFactor_mean": "Mean FF",
    #                            "FillFactor_std": "Stdev FF"
    #                            }).to_excel("results_mean.xlsx")
    return df_avg


def efficiency_results(df_select, df_reference):
    if df_select.empty or df_reference.empty:  # return empty dataframe if either dataframe is empty
        return pd.DataFrame()
    df_eff = df_select.copy()
    start_vals = df_reference.loc[df_reference['Time_min'] == df_reference['Time_min'].min()]  # need to fix!!!
    for col in ["Voc", "Isc", "FillFactor", "MaxPower", "Temperature", "Irradiance"]:
        df_eff[col + "_std"] = 100 * df_eff[col + "_std"] / df_eff[col + "_mean"] / 2
        df_eff[col + "_mean"] = 100 * (df_eff[col + "_mean"] - start_vals[col + "_mean"].values[0]) /\
                                start_vals[col + "_mean"].values[0]
    # if export:
    #     df_eff.rename(columns={"Timestamp_min": "Time (s)",
    #                            "MaxPower_mean": "DPmax/PV (%)",
    #                            "MaxPower_std": "Stdev DPmax/PV (%)",
    #                            "Voc_mean": "DVoc/PV (%)",
    #                            "Voc_std": "Stdev DVoc/PV (%)",
    #                            "Isc_mean": "DIsc/PV (%)",
    #                            "Isc_std": "Stdev DIsc/PV (%)",
    #                            "FillFactor_mean": "DFF/PV (%)",
    #                            "FillFactor_std": "Stdev DFF/PV (%)"
    #                            }).to_excel("results_efficiencies.xlsx")
    return df_eff


def get_results(dlist):
    results = pd.DataFrame(columns=["Time", "Experiment", "Voc", "Isc", "FillFactor", "MaxPower", "Temperature",
                                    "Irradiance"])
    for item in dlist:
        results = results.append({"Time": item.time,
                                  "Experiment": item.experiment,
                                  "Voc": item.v_oc,
                                  "Isc": item.i_sc,
                                  "FillFactor": item.fill_factor,
                                  "MaxPower": item.power_max,
                                  "Temperature": item.temperature,
                                  "Irradiance": item.irradiance},
                                 ignore_index=True)
    return results
