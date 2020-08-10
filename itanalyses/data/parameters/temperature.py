from itanalyses.data.parameters.parameter import Parameter


class Temperature(Parameter):
    def __init__(self, data_frames=None):
        super().__init__(data_frames=data_frames)

        self.label = {'raw': 'Temperature (C)',
                      'average': 'Temperature (C)',
                      'value': 'Average Temperature T_avg (C)',
                      'fitted': 'Average Temperature T_avg (C)'}

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
