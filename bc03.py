# -*- coding: utf-8 *-*
import numpy as np


class Ised:
    '''class Ised defines bc03 related variables.'''

    # bc03 envs & paths
    bc03_root_pth = None
    bc03_output_pth = None
    bc03_filters = None
    bc03_spectra = None
    bc03_iseds = None
    bc03_colors = None

    # dict for keyword mapping
    # tracks
    track = {'Padova_1994_chabrier': 0, 'Padova_1994_salpeter': 1}
    res = {'h': 0, 'l': 1}
    # star formation history
    sfh = {'Instant Burst(SSP)': 0, 'Exp_Tau': 1, 'Single Burst': 2,
                      'Constant': 3, 'Delayed': 4, 'Linear': 5}
    sfh_tau = {}  # dict maps sfh to a list contain tau
    # deal with dust
    dust_tau = []
    dust_mu = []
    # deal with redshift
    red = []
    h0 = 0.7
    o_lambda = 0.3
    # metalicity
    metalicity = {'0.0001': 0, '0.0004': 1, '0.004': 2, '0.008': 3,
                     '0.02': 4, '0.05': 5}
    met = []
    # age
    age = [0, ]

    def __init__(self, par=None):
        ##  par has a, b, c as string, d as list
        a = b = c = 0
        d = [0, ]
        # init points in parameter space from epar of pyraf
        self.sfh_tau[c] = d
        # code is those single inputs
        code = [self.track[a], self.res[b], self.sfh[c]]
        # lst is those multi inputs, iterate to expand
        temp = []  # init container
        # last element in temp: 0 - not calculated
        #                       1 - calculated
        for i in self.sfh_tau[c]:
            for j in self.dust_tau:
                for k in self.dust_mu:
                    temp.append([code[0], code[1], code[2],
                        i, j, k, ''])
        # generate rec array for accessibility
        inpt = np.array(temp,
            dtype=[('track', 'i'), ('res', 'i'), ('sfh', 'i'),
                ('s_tau', 'f'), ('d_tau', 'f'),
                ('d_mu', 'f'), ('lib_file', 's')])
        # mark down the existence of lib
        # lib_file is ised/*.ised
        # for age=0, get lib_color/*.1color,
        # for age!=0, get lib_spec/*.spec
        for e in inpt:
            # get search string
            search_key = self.gen_name(e)  # it is lib_file name
            if search_key == 'exist':
                e[-1] = search_key


class Cfg:
    '''class Cfg stores all config strs and vars'''

    # UI controls
    no_compute = True
    no_plot = True
    no_gui = True

    def __init__(self, par=None):
        self.ised = Ised(par)


# functions for manipulating the file_name and input
