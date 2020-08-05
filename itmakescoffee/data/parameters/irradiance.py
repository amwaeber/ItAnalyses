from itmakescoffee.data.parameters.parameter import Parameter


class Irradiance(Parameter):
    def __init__(self, data_frames=None, diode=None):
        super().__init__(data_frames=data_frames)

        if diode is None:
            self.label = {'raw': 'Irradiance (W/m2)',
                          'average': 'Irradiance (W/m2)',
                          'value': 'Average Irradiance I_avg (W/m2)',
                          'fitted': 'Average Irradiance I_avg (W/m2)'}
        else:
            self.label = {'raw': 'Irradiance %d (W/m2)' % diode,
                          'average': 'Irradiance %d (W/m2)' % diode,
                          'value': 'Average Irradiance I_%d_avg (W/m2)' % diode,
                          'fitted': 'Average Irradiance I_%d_avg (W/m2)' % diode}


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
