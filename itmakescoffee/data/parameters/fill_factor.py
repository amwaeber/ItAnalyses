from itmakescoffee.data.parameters.parameter import Parameter


class FillFactor(Parameter):
    def __init__(self, data_frames=None, n_frames=0):
        super().__init__(data_frames=data_frames)

        self.label = {'raw': 'Fill Factor',
                      'average': 'Fill Factor',
                      'value': 'Fill Factor',
                      'fitted': 'Fill Factor'}

        self.n_frames = n_frames

        self.value = [[0, 0]] * self.n_frames
        self.fit = [[0, 0]] * self.n_frames

    def set_value(self, voltage=None, current=None, power=None):
        for i in range(self.n_frames):
            vocisc = voltage.value[i][0] * current.value[i][0]
            if vocisc <= 0:
                self.value[i] = [0, 0]
            else:
                self.value[i] = [abs(power.value[i][0] / vocisc), 0]

    def set_fit(self, voltage=None, current=None, power=None):
        for i in range(self.n_frames):
            vocisc = voltage.fit[i][0] * current.fit[i][0]
            if vocisc <= 0:
                self.fit[i] = [0, 0]
            else:
                self.fit[i] = [abs(power.fit[i][0] / vocisc), 0]
