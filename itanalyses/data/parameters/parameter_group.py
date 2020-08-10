import pandas as pd

from itanalyses.data.parameters.parameter import Parameter


class ParameterGroup(Parameter):
    def __init__(self, parameters=None, labels=None):
        super().__init__(data_frames=None)

        labels = ['Parameter', 'Average Parameter'] if labels is None else labels
        self.label = {'raw': str(labels[0]),
                      'average': str(labels[0]),
                      'value': str(labels[1]),
                      'fitted': str(labels[1])}

        if parameters is not None:
            self.n_frames = len(parameters[0].raw_data)
            raw_parameter_data = list(map(list, zip(*[par.raw_data for par in parameters])))
            self.raw_data = [pd.concat(pars).groupby(level=0).mean() for pars in raw_parameter_data]
            self.value = [[0, 0]] * self.n_frames
            self.fit = [[0, 0]] * self.n_frames
            self.avg_data = pd.concat(self.raw_data).groupby(level=0).mean()

            self.idx_range = [[self.raw_data[i].first_valid_index(), self.raw_data[i].last_valid_index()]
                              for i in range(self.n_frames)]
            self.idx = [i[0] for i in self.idx_range]

    def set_value(self, idx_range=None, idx=None, n_points=5):
        if idx_range is None:
            if idx is None:
                idx = self.idx
            idx_range = [[max([self.idx_range[i][0], idx[i]-n_points]),
                         min([self.idx_range[i][1], idx[i]+n_points])] for i in range(self.n_frames)]
        for i in range(self.n_frames):
            ds = self.raw_data[i][idx_range[i][0]:idx_range[i][1]]
            self.value[i] = [ds.mean(), ds.std()]

    def set_fit(self, idx_range=None, idx=None, n_points=5):
        if idx_range is None:
            if idx is None:
                idx = self.idx
            idx_range = [[max([self.idx_range[i][0], idx[i]-n_points]),
                         min([self.idx_range[i][1], idx[i]+n_points])] for i in range(self.n_frames)]
        for i in range(self.n_frames):
            ds = self.raw_data[i][idx_range[i][0]:idx_range[i][1]]
            self.fit[i] = [ds.mean(), ds.std()]