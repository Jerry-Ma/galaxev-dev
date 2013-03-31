# -*- coding: utf-8 *-*
import numpy as np
import glob


class Ised:
    '''class Ised defines bc03 related variables.'''

    # bc03 envs & paths
    bc03_root_pth = None
    bc03_output_pth = None
    bc03_filters = None
    bc03_spectra = None
    bc03_iseds = 'galaxev'
    bc03_colors = None

    # filters
    flts = ['U', 'B', 'V', 'I', 'R']

    # dict for keyword mapping
    # tracks
    track = {'Padova_1994_chabrier': 0, 'Padova_1994_salpeter': 1}
    res = {'h': 0, 'l': 1}
    # star formation history
    sfh = {'Instant_Burst': 0, 'Exp_Tau': 1, 'Single_Burst': 2,
                      'Constant': 3, 'Delayed': 4, 'Linear': 5}
    s_tau = [0, ]  # list contain s_tau
    # deal with dust
    d_tau = [0, ]
    d_mu = [0, ]
    # deal with redshift
    red = []
    h0 = 0.7
    o_lambda = 0.3
    # metalicity
    metalicity = {'0.0001': 0, '0.0004': 1, '0.004': 2, '0.008': 3,
                     '0.02': 4, '0.05': 5}
    met = [0, ]
    # age
    age = [0, ]

    def __init__(self, par=None):
        ##  par has a, b, c as string, d as list
        a = 'Padova_1994_chabrier'
        b = 'h'
        c = 'Instant_Burst'
        self.code_txt = a + '__' + b + '__' + c
        self.s_tau = np.arange(0.1, 0.9, 0.2)  # sfh_tau
        self.d_tau = np.arange(0.1, 0.9, 0.4)
        self.d_mu = np.arange(0.1, 0.9, 0.1)
        self.met = np.array([0.0001, 0.0004, 0.004, 0.008,
                     0.02, 0.05])
        self.age = np.arange(1.0, 20.0, 1.0)
        # init points in parameter space from epar of pyraf
        # code is those single inputs
        code = [self.track[a], self.res[b], self.sfh[c]]
        # lst is those multi inputs, iterate to expand
        temp = []  # init container
        # last element in temp: 0 - not calculated
        #                       1 - calculated
        for i in self.s_tau:
            for j in self.d_tau:
                for k in self.d_mu:
                    for l in self.met:
                        for m in self.age:
                            temp.append((code[0], code[1], code[2],
                                i, j, k, l, m, 0))
        # generate rec array for accessibility
        self.parspace = np.array(temp,
            dtype=[('track', 'i'), ('res', 'i'), ('sfh', 'i'),
                ('s_tau', 'f'), ('d_tau', 'f'), ('d_mu', 'f'),
                ('met', 'f'), ('age', 'f'), ('exist', 'i')])
        # mark down the existence of lib
        # lib_file is ised/*.ised
        # for age=0, get lib_color/*.1color,
        # for age!=0, get lib_spec/*.spec
        for e in self.parspace:
            # get search string
            filename, exist = self.gen_name(e)  # it is lib_file name
            e[-1] = exist
    # functions for manipulating the file_name and input

    def gen_name(self, e):
        filename = self.track.keys()[self.track.values().index(e[0])] + '__' +\
            self.res.keys()[self.res.values().index(e[1])] + '__' +\
            self.sfh.keys()[self.sfh.values().index(e[2])] + '__' +\
            str(e[3]) + '__' + str(e[4]) + '__' + str(e[5]) + '__' +\
            str(e[6]) + '.ised'
        exist = len(glob.glob(self.bc03_iseds + filename))
        return filename, exist


class Cfg:
    '''class Cfg stores all config strs and vars'''

    # UI controls
    no_compute = True
    no_plot = True
    no_gui = True

    def __init__(self, par=None):
        self.ised = Ised(par)